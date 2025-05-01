#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <libgen.h>
#include <unistd.h>
#include <ctype.h>
#include <pwd.h>
#include <limits.h>
#include "../include/directory_handler.h"

#define MAX_PATHS 2048
#define MAX_PATH_LEN 4096
#define MAX_ALTERNATIVES 256

/**
 * Structure pour stocker les alternatives d'expansion
 */
typedef struct {
    char *alternatives[MAX_ALTERNATIVES];
    int count;
} expansion_alternatives_t;

/**
 * Détermine si un chemin se termine par un slash (/)
 * @param path Le chemin à vérifier
 * @return 1 si le chemin se termine par /, 0 sinon
 */
static int is_directory_path(const char *path) {
    size_t len = strlen(path);
    return (len > 0 && path[len - 1] == '/');
}

/**
 * Crée un fichier vide et tous les répertoires parents
 * @param path Le chemin du fichier à créer
 * @return 0 en cas de succès, -1 en cas d'erreur
 */
static int create_file(const char *path) {
    // Vérifier si l'opération est limitée au répertoire home
    if (is_home_directory_restriction()) {
        if (!is_path_in_home_directory(path)) {
            if (!is_quiet_mode()) {
                fprintf(stderr, "Erreur de sécurité: Le chemin '%s' est en dehors de votre répertoire personnel.\n", path);
                fprintf(stderr, "Les opérations sont restreintes à votre répertoire personnel pour des raisons de sécurité.\n");
            }
            return -1;
        }
    }

    char *dir_path = strdup(path);
    if (!dir_path) {
        fprintf(stderr, "Memory allocation error when creating file: %s\n", path);
        return -1;
    }

    char *dir_name = dirname(dir_path);
    
    // Créer les répertoires parents
    int status = create_directory_recursive(dir_name);
    free(dir_path);
    
    if (status != 0) {
        return -1;
    }
    
    // Créer le fichier
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        fprintf(stderr, "Failed to create file '%s': %s\n", path, strerror(errno));
        return -1;
    }
    
    fclose(file);
    return 0;
}

/**
 * Identifie les accolades correspondantes et gère les niveaux d'imbrication
 * @param path Le chemin à analyser
 * @param start_pos Position de début de la recherche
 * @param open_pos Position retournée de l'accolade ouvrante ou -1
 * @param close_pos Position retournée de l'accolade fermante ou -1
 * @return 1 si une paire d'accolades a été trouvée, 0 sinon
 */
static int find_matching_braces(const char *path, int start_pos, int *open_pos, int *close_pos) {
    int i = start_pos;
    int len = strlen(path);
    
    // Initialiser les positions à -1 (non trouvé)
    *open_pos = -1;
    *close_pos = -1;
    
    // Chercher l'accolade ouvrante à partir de start_pos
    while (i < len) {
        if (path[i] == '{') {
            *open_pos = i;
            break;
        }
        i++;
    }
    
    // Si pas d'accolade ouvrante, retourner 0
    if (*open_pos == -1) {
        return 0;
    }
    
    // Trouver l'accolade fermante correspondante en tenant compte des imbrications
    int level = 1;
    i = *open_pos + 1;
    
    while (i < len && level > 0) {
        if (path[i] == '{') {
            level++;
        } else if (path[i] == '}') {
            level--;
            if (level == 0) {
                *close_pos = i;
                return 1;
            }
        }
        i++;
    }
    
    // Si pas d'accolade fermante correspondante, signaler l'erreur
    fprintf(stderr, "Error: Unclosed brace at position %d in path: %s\n", *open_pos, path);
    return 0;
}

/**
 * Extrait les alternatives d'un contenu entre accolades
 * @param content Le contenu entre accolades (sans les accolades)
 * @param alternatives Structure pour stocker les alternatives extraites
 * @return 0 en cas de succès, -1 en cas d'erreur
 */
static int extract_alternatives(const char *content, expansion_alternatives_t *alternatives) {
    // Réinitialiser le compteur d'alternatives
    alternatives->count = 0;
    
    // Copier le contenu pour éviter de modifier l'original
    char *content_copy = strdup(content);
    if (!content_copy) {
        fprintf(stderr, "Memory allocation error when extracting alternatives\n");
        return -1;
    }
    
    // Analyser manuellement pour extraire les alternatives
    int start = 0;
    int i = 0;
    int level = 0;
    int content_len = strlen(content_copy);
    
    while (i <= content_len) {
        // Virgule au niveau 0 ou fin de chaîne = séparateur d'alternative
        if ((i == content_len || (content_copy[i] == ',' && level == 0)) && i > start) {
            // Créer une nouvelle alternative
            int alt_len = i - start;
            
            if (alternatives->count >= MAX_ALTERNATIVES) {
                fprintf(stderr, "Too many alternatives in brace expansion\n");
                free(content_copy);
                return -1;
            }
            
            char *alt = malloc(alt_len + 1);
            if (!alt) {
                fprintf(stderr, "Memory allocation error\n");
                free(content_copy);
                return -1;
            }
            
            // Copier l'alternative
            strncpy(alt, content_copy + start, alt_len);
            alt[alt_len] = '\0';
            
            alternatives->alternatives[alternatives->count++] = alt;
            
            // Passer à l'alternative suivante
            if (i < content_len && content_copy[i] == ',') {
                start = i + 1;
            }
        } else if (content_copy[i] == '{') {
            level++;
        } else if (content_copy[i] == '}') {
            level--;
        }
        
        i++;
    }
    
    free(content_copy);
    return 0;
}

/**
 * Libère la mémoire allouée pour les alternatives
 * @param alternatives Structure contenant les alternatives à libérer
 */
static void free_alternatives(expansion_alternatives_t *alternatives) {
    for (int i = 0; i < alternatives->count; i++) {
        if (alternatives->alternatives[i]) {
            free(alternatives->alternatives[i]);
            alternatives->alternatives[i] = NULL;
        }
    }
    alternatives->count = 0;
}

/**
 * Traite un chemin et génère tous les chemins possibles après expansion des accolades
 * @param path Le chemin d'entrée avec accolades
 * @param paths Tableau pour stocker les chemins générés
 * @param path_count Nombre de chemins générés (actualisé)
 * @param max_paths Nombre maximum de chemins que le tableau peut contenir
 * @return 0 en cas de succès, -1 en cas d'erreur
 */
static int expand_braces(const char *path, char paths[][MAX_PATH_LEN], int *path_count, int max_paths) {
    // Chercher les accolades dans le chemin
    int open_pos, close_pos;
    
    if (!find_matching_braces(path, 0, &open_pos, &close_pos)) {
        // Pas d'accolades, ajouter directement le chemin
        if (*path_count < max_paths) {
            strncpy(paths[*path_count], path, MAX_PATH_LEN - 1);
            paths[*path_count][MAX_PATH_LEN - 1] = '\0';
            (*path_count)++;
            return 0;
        } else {
            fprintf(stderr, "Too many paths generated (limit: %d)\n", max_paths);
            return -1;
        }
    }
    
    // Extraire les parties du chemin
    char prefix[MAX_PATH_LEN] = {0};
    char content[MAX_PATH_LEN] = {0};
    char suffix[MAX_PATH_LEN] = {0};
    
    // Construire le préfixe (partie avant les accolades)
    if (open_pos > 0) {
        strncpy(prefix, path, open_pos);
        prefix[open_pos] = '\0';
    }
    
    // Extraire le contenu entre accolades
    strncpy(content, path + open_pos + 1, close_pos - open_pos - 1);
    content[close_pos - open_pos - 1] = '\0';
    
    // Construire le suffixe (partie après les accolades)
    strcpy(suffix, path + close_pos + 1);
    
    // Extraire les alternatives du contenu
    expansion_alternatives_t alternatives = {0};
    if (extract_alternatives(content, &alternatives) != 0) {
        return -1;
    }
    
    // Si aucune alternative n'a été trouvée, traiter la chaîne comme une seule alternative
    if (alternatives.count == 0) {
        char *alt = strdup(content);
        if (!alt) {
            fprintf(stderr, "Memory allocation error\n");
            return -1;
        }
        alternatives.alternatives[alternatives.count++] = alt;
    }
    
    // Pour chaque alternative, construire un nouveau chemin et l'expanser récursivement
    for (int i = 0; i < alternatives.count; i++) {
        char new_path[MAX_PATH_LEN];
        
        // Vérifier si la combinaison des chemins ne dépasse pas la taille maximale
        size_t prefix_len = strlen(prefix);
        size_t alt_len = strlen(alternatives.alternatives[i]);
        size_t suffix_len = strlen(suffix);
        
        // Vérifier que la longueur totale ne dépasse pas MAX_PATH_LEN-1 (pour le \0)
        if (prefix_len + alt_len + suffix_len >= MAX_PATH_LEN - 1) {
            fprintf(stderr, "Path too long: %s%s%s\n", prefix, alternatives.alternatives[i], suffix);
            free_alternatives(&alternatives);
            return -1;
        }
        
        // Construire le nouveau chemin de manière sécurisée
        new_path[0] = '\0';
        strcat(new_path, prefix);
        strcat(new_path, alternatives.alternatives[i]);
        strcat(new_path, suffix);
        
        // Traiter récursivement ce nouveau chemin
        if (expand_braces(new_path, paths, path_count, max_paths) != 0) {
            free_alternatives(&alternatives);
            return -1;
        }
    }
    
    // Libérer la mémoire des alternatives
    free_alternatives(&alternatives);
    return 0;
}

int create_directory_recursive(const char *path) {
    if (!path || strlen(path) == 0) {
        return -1;
    }

    // Vérifier si l'opération est limitée au répertoire home
    if (is_home_directory_restriction()) {
        if (!is_path_in_home_directory(path)) {
            if (!is_quiet_mode()) {
                fprintf(stderr, "Erreur de sécurité: Le chemin '%s' est en dehors de votre répertoire personnel.\n", path);
                fprintf(stderr, "Les opérations sont restreintes à votre répertoire personnel pour des raisons de sécurité.\n");
            }
            return -1;
        }
    }

    char *path_copy;
    char *p;
    int status = 0;
    struct stat st;

    // Vérifier si le répertoire existe déjà
    if (stat(path, &st) == 0) {
        if (S_ISDIR(st.st_mode)) {
            return 0; // Le répertoire existe déjà
        }
        return -1; // Le chemin existe mais n'est pas un répertoire
    }
    
    // Créer une copie du chemin pour éviter de modifier l'original
    path_copy = strdup(path);
    if (path_copy == NULL) {
        perror("Failed to allocate memory for path");
        return -1;
    }

    // Créer les répertoires parents récursivement
    for (p = path_copy + 1; *p; p++) {
        if (*p == '/') {
            *p = '\0'; // Terminer temporairement la chaîne
            if (mkdir(path_copy, 0755) != 0 && errno != EEXIST) {
                fprintf(stderr, "Failed to create directory '%s': %s\n", path_copy, strerror(errno));
                status = -1;
                break;
            }
            *p = '/'; // Restaurer le slash
        }
    }

    if (status == 0) {
        // Créer le répertoire final
        if (mkdir(path_copy, 0755) != 0 && errno != EEXIST) {
            fprintf(stderr, "Failed to create directory '%s': %s\n", path_copy, strerror(errno));
            status = -1;
        }
    }

    free(path_copy);
    return status;
}

int create_directory_structure(const char *path) {
    // Valider l'entrée
    if (path == NULL || path[0] == '\0') {
        fprintf(stderr, "Invalid path\n");
        return EXIT_FAILURE;
    }

    // Obtenir le répertoire de travail actuel pour la confirmation
    char cwd[MAX_PATH_LEN];
    if (getcwd(cwd, sizeof(cwd)) == NULL) {
        if (!is_quiet_mode()) {
            fprintf(stderr, "Impossible d'obtenir le répertoire courant\n");
        }
        // Continuer malgré l'erreur
        strcpy(cwd, "répertoire courant");
    }

    // Préparer la variable pour stocker le chemin de base final
    char base_path[MAX_PATH_LEN] = "";
    
    // Demander confirmation sauf en mode silencieux ou en mode force
    if (!is_quiet_mode() && !is_force_mode()) {
        printf("Vous allez générer ce projet ici : %s\n", cwd);
        printf("Êtes-vous sûr ? (O/n/chemin) : ");
        fflush(stdout);
        
        // Lire la réponse de l'utilisateur
        char response_buffer[MAX_PATH_LEN];
        if (fgets(response_buffer, sizeof(response_buffer), stdin) == NULL) {
            printf("Erreur de lecture de la réponse. Opération annulée.\n");
            return EXIT_SUCCESS;
        }
        
        // Supprimer le retour à la ligne final si présent
        size_t len = strlen(response_buffer);
        if (len > 0 && response_buffer[len - 1] == '\n') {
            response_buffer[len - 1] = '\0';
            len--;
        }
        
        // Analyser la réponse
        if (len == 0 || response_buffer[0] == 'O' || response_buffer[0] == 'o') {
            // Utiliser le répertoire courant (comportement par défaut)
            strcpy(base_path, "");
        } else if (response_buffer[0] == 'n' || response_buffer[0] == 'N') {
            printf("Opération annulée.\n");
            return EXIT_SUCCESS;
        } else {
            // La réponse est considérée comme un chemin alternatif ou une demande de chemin
            
            // Vérifier si l'utilisateur a simplement entré "chemin" ou un mot similaire
            if (strcmp(response_buffer, "chemin") == 0 || strcmp(response_buffer, "path") == 0 || 
                strcmp(response_buffer, "dossier") == 0 || strcmp(response_buffer, "folder") == 0) {
                // L'utilisateur a entré "chemin" au lieu d'un vrai chemin, lui demander explicitement
                printf("Veuillez entrer le chemin où vous souhaitez créer le projet : ");
                fflush(stdout);
                
                if (fgets(response_buffer, sizeof(response_buffer), stdin) == NULL) {
                    printf("Erreur de lecture du chemin. Opération annulée.\n");
                    return EXIT_SUCCESS;
                }
                
                // Supprimer le retour à la ligne final
                len = strlen(response_buffer);
                if (len > 0 && response_buffer[len - 1] == '\n') {
                    response_buffer[len - 1] = '\0';
                    len--;
                }
                
                if (len == 0) {
                    printf("Aucun chemin spécifié. Opération annulée.\n");
                    return EXIT_SUCCESS;
                }
            }

            // Si le chemin entré ne contient pas de slash à la fin, ajouter un
            len = strlen(response_buffer);
            if (len > 0 && response_buffer[len - 1] != '/') {
                response_buffer[len] = '/';
                response_buffer[len + 1] = '\0';
            }
            
            // Vérifier si le chemin semble valide (contient au moins un '/')
            if (strchr(response_buffer, '/') == NULL) {
                printf("Le chemin entré ne semble pas valide. Un chemin doit contenir au moins un '/'\n");
                printf("Exemple: /chemin/vers/dossier/ ou ./dossier/ ou ~/dossier/\n");
                printf("Voulez-vous réessayer ? (O/n) : ");
                fflush(stdout);
                
                char retry_response;
                scanf(" %c", &retry_response);
                while (getchar() != '\n'); // Nettoyer le buffer d'entrée
                
                if (retry_response == 'O' || retry_response == 'o') {
                    printf("Veuillez entrer le chemin complet : ");
                    fflush(stdout);
                    
                    if (fgets(response_buffer, sizeof(response_buffer), stdin) == NULL) {
                        printf("Erreur de lecture du chemin. Opération annulée.\n");
                        return EXIT_SUCCESS;
                    }
                    
                    // Supprimer le retour à la ligne final
                    len = strlen(response_buffer);
                    if (len > 0 && response_buffer[len - 1] == '\n') {
                        response_buffer[len - 1] = '\0';
                        len--;
                    }
                    
                    // Ajouter un slash à la fin si nécessaire
                    if (len > 0 && response_buffer[len - 1] != '/') {
                        response_buffer[len] = '/';
                        response_buffer[len + 1] = '\0';
                    }
                } else {
                    printf("Opération annulée.\n");
                    return EXIT_SUCCESS;
                }
            }
            
            // Étendre le chemin (développer ~, etc.) si nécessaire
            if (response_buffer[0] == '~') {
                if (expand_tilde(response_buffer, base_path, sizeof(base_path)) != 0) {
                    fprintf(stderr, "Erreur lors de l'expansion du chemin: %s\n", response_buffer);
                    return EXIT_FAILURE;
                }
            } else {
                strcpy(base_path, response_buffer);
            }
            
            printf("Le projet sera créé dans : %s\n", base_path);
            
            // Créer le répertoire de base s'il n'existe pas
            if (strlen(base_path) > 0) {
                struct stat st;
                if (stat(base_path, &st) != 0) {
                    // Le répertoire n'existe pas, on demande s'il faut le créer
                    printf("Le répertoire '%s' n'existe pas. Voulez-vous le créer ? (O/n) : ", base_path);
                    fflush(stdout);
                    
                    char create_dir_response;
                    scanf(" %c", &create_dir_response);
                    while (getchar() != '\n'); // Nettoyer le buffer d'entrée
                    
                    if (create_dir_response != 'O' && create_dir_response != 'o') {
                        printf("Opération annulée.\n");
                        return EXIT_SUCCESS;
                    }
                    
                    if (create_directory_recursive(base_path) != 0) {
                        fprintf(stderr, "Échec de la création du répertoire '%s'\n", base_path);
                        return EXIT_FAILURE;
                    }
                    printf("Répertoire '%s' créé avec succès.\n", base_path);
                }
            }
        }
    }

    // Initialiser le compteur de chemins générés
    int path_count = 0;
    
    // Allouer la mémoire pour les chemins expansés
    char (*paths)[MAX_PATH_LEN] = calloc(MAX_PATHS, sizeof(char[MAX_PATH_LEN]));
    if (!paths) {
        fprintf(stderr, "Memory allocation error\n");
        return EXIT_FAILURE;
    }
    
    // Expanser les accolades pour générer tous les chemins possibles
    if (expand_braces(path, paths, &path_count, MAX_PATHS) != 0) {
        free(paths);
        return EXIT_FAILURE;
    }
    
    // Créer chaque chemin
    for (int i = 0; i < path_count; i++) {
        // Construire le chemin complet avec le préfixe si nécessaire
        char full_path[MAX_PATH_LEN];
        if (strlen(base_path) > 0) {
            snprintf(full_path, sizeof(full_path), "%s%s", base_path, paths[i]);
        } else {
            strcpy(full_path, paths[i]);
        }
        
        // Vérifier si l'opération est limitée au répertoire home
        if (is_home_directory_restriction()) {
            if (!is_path_in_home_directory(full_path)) {
                if (!is_quiet_mode()) {
                    fprintf(stderr, "Erreur de sécurité: Le chemin '%s' est en dehors de votre répertoire personnel.\n", full_path);
                    fprintf(stderr, "Les opérations sont restreintes à votre répertoire personnel pour des raisons de sécurité.\n");
                }
                continue; // Ignorer ce chemin et passer au suivant
            }
        }
        
        // Vérifier si c'est un template de fichier (format: fichier.txt:template.txt)
        if (is_template_path(full_path)) {
            char dest_path[MAX_PATH_LEN];
            char template_path[MAX_PATH_LEN];
            
            // Extraire les informations du template
            if (extract_template_info(full_path, dest_path, template_path, MAX_PATH_LEN) != 0) {
                fprintf(stderr, "Failed to parse template path: %s\n", full_path);
                continue;
            }
            
            // Créer le fichier à partir du template
            if (create_file_from_template(dest_path, template_path) != 0) {
                fprintf(stderr, "Failed to create file from template: %s (template: %s)\n", dest_path, template_path);
                // Continuer avec les autres chemins
            } else {
                if (!is_quiet_mode()) {
                    printf("Created file from template: %s\n", dest_path);
                }
            }
        }
        // Si c'est un chemin se terminant par /, c'est un répertoire
        else if (is_directory_path(full_path)) {
            if (create_directory_recursive(full_path) != 0) {
                if (!is_quiet_mode()) {
                    fprintf(stderr, "Failed to create directory: %s\n", full_path);
                }
                // Continuer avec les autres chemins
            } else if (!is_quiet_mode()) {
                printf("Created directory: %s\n", full_path);
            }
        } 
        // Pas de slash final, c'est un fichier
        else {
            if (create_file(full_path) != 0) {
                if (!is_quiet_mode()) {
                    fprintf(stderr, "Failed to create file: %s\n", full_path);
                }
                // Continuer avec les autres chemins
            } else if (!is_quiet_mode()) {
                printf("Created file: %s\n", full_path);
            }
        }
    }
    
    free(paths);
    return EXIT_SUCCESS;
}

// Structure templates
static const char *template_backend[] = {
    "/app",
    "/app/api",
    "/app/api/v1",
    "/app/api/v1/endpoints",
    "/app/api/v1/endpoints/users",
    "/app/api/v1/endpoints/feature1",
    "/app/api/v1/endpoints/feature2",
    "/app/api/router",
    "/app/api/router/deps",
    "/app/api/router/router",
    "/app/service",
    "/app/models",
    "/app/utils",
    NULL
};

static const char *template_frontend[] = {
    "/src",
    "/src/components",
    "/src/store",
    "/src/router",
    "/src/views",
    NULL
};

// Structure templates pour React
static const char *template_react[] = {
    "/public",
    "/src",
    "/src/components",
    "/src/hooks",
    "/src/pages",
    "/src/assets",
    "/src/contexts",
    NULL
};

// Structure templates pour Flask
static const char *template_flask[] = {
    "/app",
    "/app/static",
    "/app/static/css",
    "/app/static/js",
    "/app/static/img",
    "/app/templates",
    "/app/routes",
    "/app/models",
    "/app/utils",
    "/tests",
    NULL
};

// Create frontend files
static void create_frontend_files(const char *project_path) {
    char file_path[1024];
    FILE *file;
    
    // Create App.vue
    snprintf(file_path, sizeof(file_path), "%s/src/App.vue", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "<template>\n  <div id=\"app\">\n    <h1>Welcome to Your Vue.js App</h1>\n  </div>\n</template>\n\n");
        fprintf(file, "<script>\nexport default {\n  name: 'App'\n}\n</script>\n\n");
        fprintf(file, "<style>\n#app {\n  font-family: 'Avenir', Helvetica, Arial, sans-serif;\n}\n</style>\n");
        fclose(file);
    }
    
    // Create main.js
    snprintf(file_path, sizeof(file_path), "%s/src/main.js", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "import { createApp } from 'vue'\n");
        fprintf(file, "import App from './App.vue'\n\n");
        fprintf(file, "createApp(App).mount('#app')\n");
        fclose(file);
    }
    
    // Create package.json
    snprintf(file_path, sizeof(file_path), "%s/package.json", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "{\n");
        fprintf(file, "  \"name\": \"frontend\",\n");
        fprintf(file, "  \"version\": \"0.1.0\",\n");
        fprintf(file, "  \"private\": true,\n");
        fprintf(file, "  \"scripts\": {\n");
        fprintf(file, "    \"dev\": \"vite\",\n");
        fprintf(file, "    \"build\": \"vite build\",\n");
        fprintf(file, "    \"preview\": \"vite preview\"\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"dependencies\": {\n");
        fprintf(file, "    \"vue\": \"^3.3.4\"\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"devDependencies\": {\n");
        fprintf(file, "    \"@vitejs/plugin-vue\": \"^4.2.3\",\n");
        fprintf(file, "    \"vite\": \"^4.4.6\"\n");
        fprintf(file, "  }\n");
        fprintf(file, "}\n");
        fclose(file);
    }
    
    // Create vite.config.js
    snprintf(file_path, sizeof(file_path), "%s/vite.config.js", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "import { defineConfig } from 'vite'\n");
        fprintf(file, "import vue from '@vitejs/plugin-vue'\n\n");
        fprintf(file, "// https://vitejs.dev/config/\n");
        fprintf(file, "export default defineConfig({\n");
        fprintf(file, "  plugins: [vue()],\n");
        fprintf(file, "})\n");
        fclose(file);
    }
}

// Create backend files
static void create_backend_files(const char *project_path) {
    char file_path[1024];
    FILE *file;
    
    // Create main.py
    snprintf(file_path, sizeof(file_path), "%s/app/main.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "from fastapi import FastAPI\n\n");
        fprintf(file, "app = FastAPI(title=\"FastAPI Application\")\n\n");
        fprintf(file, "# Import routers\n");
        fprintf(file, "from api.v1.endpoints import users, feature1, feature2\n\n");
        fprintf(file, "# Include routers\n");
        fprintf(file, "app.include_router(users.router, prefix=\"/api/v1\")\n");
        fprintf(file, "app.include_router(feature1.router, prefix=\"/api/v1\")\n");
        fprintf(file, "app.include_router(feature2.router, prefix=\"/api/v1\")\n\n");
        fprintf(file, "@app.get(\"/\")\n");
        fprintf(file, "def read_root():\n");
        fprintf(file, "    return {\"message\": \"Welcome to the API\"}\n\n");
        fprintf(file, "if __name__ == \"__main__\":\n");
        fprintf(file, "    import uvicorn\n");
        fprintf(file, "    uvicorn.run(\"main:app\", host=\"0.0.0.0\", port=8000, reload=True)\n");
        fclose(file);
    }
    
    // Create users.py
    snprintf(file_path, sizeof(file_path), "%s/app/api/v1/endpoints/users.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "from fastapi import APIRouter\n\n");
        fprintf(file, "router = APIRouter(tags=[\"users\"])\n\n");
        fprintf(file, "@router.get(\"/users\")\n");
        fprintf(file, "def get_users():\n");
        fprintf(file, "    return {\"users\": [\"user1\", \"user2\"]}\n");
        fclose(file);
    }
    
    // Create __init__.py files to make Python packages
    const char *init_dirs[] = {
        "/app",
        "/app/api",
        "/app/api/v1",
        "/app/api/v1/endpoints",
        "/app/api/router",
        "/app/service",
        "/app/models",
        "/app/utils",
        NULL
    };
    
    for (int i = 0; init_dirs[i] != NULL; i++) {
        char init_path[1024];
        snprintf(init_path, sizeof(init_path), "%s%s/__init__.py", project_path, init_dirs[i]);
        file = fopen(init_path, "w");
        if (file) {
            fclose(file);
        }
    }
}

// Créer les fichiers React
static void create_react_files(const char *project_path) {
    char file_path[1024];
    FILE *file;
    
    // Créer le fichier package.json
    snprintf(file_path, sizeof(file_path), "%s/package.json", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "{\n");
        fprintf(file, "  \"name\": \"react-app\",\n");
        fprintf(file, "  \"version\": \"0.1.0\",\n");
        fprintf(file, "  \"private\": true,\n");
        fprintf(file, "  \"dependencies\": {\n");
        fprintf(file, "    \"react\": \"^18.2.0\",\n");
        fprintf(file, "    \"react-dom\": \"^18.2.0\",\n");
        fprintf(file, "    \"react-router-dom\": \"^6.16.0\",\n");
        fprintf(file, "    \"react-scripts\": \"5.0.1\"\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"scripts\": {\n");
        fprintf(file, "    \"start\": \"react-scripts start\",\n");
        fprintf(file, "    \"build\": \"react-scripts build\",\n");
        fprintf(file, "    \"test\": \"react-scripts test\",\n");
        fprintf(file, "    \"eject\": \"react-scripts eject\"\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"eslintConfig\": {\n");
        fprintf(file, "    \"extends\": [\n");
        fprintf(file, "      \"react-app\",\n");
        fprintf(file, "      \"react-app/jest\"\n");
        fprintf(file, "    ]\n");
        fprintf(file, "  },\n");
        fprintf(file, "  \"browserslist\": {\n");
        fprintf(file, "    \"production\": [\n");
        fprintf(file, "      \">0.2%%\",\n");
        fprintf(file, "      \"not dead\",\n");
        fprintf(file, "      \"not op_mini all\"\n");
        fprintf(file, "    ],\n");
        fprintf(file, "    \"development\": [\n");
        fprintf(file, "      \"last 1 chrome version\",\n");
        fprintf(file, "      \"last 1 firefox version\",\n");
        fprintf(file, "      \"last 1 safari version\"\n");
        fprintf(file, "    ]\n");
        fprintf(file, "  }\n");
        fprintf(file, "}\n");
        fclose(file);
    }
    
    // Créer index.html
    snprintf(file_path, sizeof(file_path), "%s/public/index.html", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "<!DOCTYPE html>\n");
        fprintf(file, "<html lang=\"en\">\n");
        fprintf(file, "  <head>\n");
        fprintf(file, "    <meta charset=\"utf-8\" />\n");
        fprintf(file, "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n");
        fprintf(file, "    <title>React App</title>\n");
        fprintf(file, "  </head>\n");
        fprintf(file, "  <body>\n");
        fprintf(file, "    <noscript>You need to enable JavaScript to run this app.</noscript>\n");
        fprintf(file, "    <div id=\"root\"></div>\n");
        fprintf(file, "  </body>\n");
        fprintf(file, "</html>\n");
        fclose(file);
    }
    
    // Créer App.js
    snprintf(file_path, sizeof(file_path), "%s/src/App.js", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "import React from 'react';\n");
        fprintf(file, "import './App.css';\n\n");
        fprintf(file, "function App() {\n");
        fprintf(file, "  return (\n");
        fprintf(file, "    <div className=\"App\">\n");
        fprintf(file, "      <header className=\"App-header\">\n");
        fprintf(file, "        <h1>Welcome to React</h1>\n");
        fprintf(file, "        <p>\n");
        fprintf(file, "          Edit <code>src/App.js</code> and save to reload.\n");
        fprintf(file, "        </p>\n");
        fprintf(file, "      </header>\n");
        fprintf(file, "    </div>\n");
        fprintf(file, "  );\n");
        fprintf(file, "}\n\n");
        fprintf(file, "export default App;\n");
        fclose(file);
    }
    
    // Créer index.js
    snprintf(file_path, sizeof(file_path), "%s/src/index.js", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "import React from 'react';\n");
        fprintf(file, "import ReactDOM from 'react-dom/client';\n");
        fprintf(file, "import './index.css';\n");
        fprintf(file, "import App from './App';\n\n");
        fprintf(file, "const root = ReactDOM.createRoot(document.getElementById('root'));\n");
        fprintf(file, "root.render(\n");
        fprintf(file, "  <React.StrictMode>\n");
        fprintf(file, "    <App />\n");
        fprintf(file, "  </React.StrictMode>\n");
        fprintf(file, ");\n");
        fclose(file);
    }
    
    // Créer App.css
    snprintf(file_path, sizeof(file_path), "%s/src/App.css", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, ".App {\n");
        fprintf(file, "  text-align: center;\n");
        fprintf(file, "}\n\n");
        fprintf(file, ".App-header {\n");
        fprintf(file, "  background-color: #282c34;\n");
        fprintf(file, "  min-height: 100vh;\n");
        fprintf(file, "  display: flex;\n");
        fprintf(file, "  flex-direction: column;\n");
        fprintf(file, "  align-items: center;\n");
        fprintf(file, "  justify-content: center;\n");
        fprintf(file, "  font-size: calc(10px + 2vmin);\n");
        fprintf(file, "  color: white;\n");
        fclose(file);
    }
    
    // Créer index.css
    snprintf(file_path, sizeof(file_path), "%s/src/index.css", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "body {\n");
        fprintf(file, "  margin: 0;\n");
        fprintf(file, "  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',\n");
        fprintf(file, "    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',\n");
        fprintf(file, "    sans-serif;\n");
        fprintf(file, "  -webkit-font-smoothing: antialiased;\n");
        fprintf(file, "  -moz-osx-font-smoothing: grayscale;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "code {\n");
        fprintf(file, "  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',\n");
        fprintf(file, "    monospace;\n");
        fprintf(file, "}\n");
        fclose(file);
    }
}

// Créer les fichiers Flask
static void create_flask_files(const char *project_path) {
    char file_path[1024];
    FILE *file;
    
    // Créer requirements.txt
    snprintf(file_path, sizeof(file_path), "%s/requirements.txt", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "Flask==2.3.3\n");
        fprintf(file, "Werkzeug==2.3.7\n");
        fprintf(file, "Jinja2==3.1.2\n");
        fprintf(file, "Flask-SQLAlchemy==3.1.1\n");
        fprintf(file, "pytest==7.4.0\n");
        fclose(file);
    }
    
    // Créer __init__.py principal
    snprintf(file_path, sizeof(file_path), "%s/app/__init__.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "from flask import Flask\n");
        fprintf(file, "from flask_sqlalchemy import SQLAlchemy\n\n");
        fprintf(file, "db = SQLAlchemy()\n\n");
        fprintf(file, "def create_app(config_name='default'):\n");
        fprintf(file, "    app = Flask(__name__)\n");
        fprintf(file, "    \n");
        fprintf(file, "    # Configuration\n");
        fprintf(file, "    if config_name == 'production':\n");
        fprintf(file, "        app.config.from_object('app.config.ProductionConfig')\n");
        fprintf(file, "    elif config_name == 'testing':\n");
        fprintf(file, "        app.config.from_object('app.config.TestingConfig')\n");
        fprintf(file, "    else:\n");
        fprintf(file, "        app.config.from_object('app.config.DevelopmentConfig')\n");
        fprintf(file, "    \n");
        fprintf(file, "    # Initialize extensions\n");
        fprintf(file, "    db.init_app(app)\n");
        fprintf(file, "    \n");
        fprintf(file, "    # Register blueprints\n");
        fprintf(file, "    from app.routes.main import main_bp\n");
        fprintf(file, "    app.register_blueprint(main_bp)\n");
        fprintf(file, "    \n");
        fprintf(file, "    return app\n");
        fclose(file);
    }
    
    // Créer routes/main.py
    snprintf(file_path, sizeof(file_path), "%s/app/routes/__init__.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "# Routes package\n");
        fclose(file);
    }
    
    snprintf(file_path, sizeof(file_path), "%s/app/routes/main.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "from flask import Blueprint, render_template\n\n");
        fprintf(file, "main_bp = Blueprint('main', __name__)\n\n");
        fprintf(file, "@main_bp.route('/')\n");
        fprintf(file, "def index():\n");
        fprintf(file, "    return render_template('index.html')\n");
        fclose(file);
    }
    
    // Créer models/__init__.py
    snprintf(file_path, sizeof(file_path), "%s/app/models/__init__.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "# Import models here to make them available\n");
        fprintf(file, "# Example: from app.models.user import User\n");
        fclose(file);
    }
    
    // Créer utils/__init__.py
    snprintf(file_path, sizeof(file_path), "%s/app/utils/__init__.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "# Utility functions\n");
        fclose(file);
    }
    
    // Créer config.py
    snprintf(file_path, sizeof(file_path), "%s/app/config.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "class Config(object):\n");
        fprintf(file, "    DEBUG = False\n");
        fprintf(file, "    TESTING = False\n");
        fprintf(file, "    SECRET_KEY = 'your-secret-key'\n");
        fprintf(file, "    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'\n");
        fprintf(file, "    SQLALCHEMY_TRACK_MODIFICATIONS = False\n\n");
        fprintf(file, "class DevelopmentConfig(Config):\n");
        fprintf(file, "    DEBUG = True\n\n");
        fprintf(file, "class TestingConfig(Config):\n");
        fprintf(file, "    TESTING = True\n");
        fprintf(file, "    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'\n\n");
        fprintf(file, "class ProductionConfig(Config):\n");
        fprintf(file, "    pass\n");
        fclose(file);
    }
    
    // Créer run.py
    snprintf(file_path, sizeof(file_path), "%s/run.py", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "from app import create_app\n\n");
        fprintf(file, "app = create_app()\n\n");
        fprintf(file, "if (file == '__main__'):\n");
        fprintf(file, "    app.run(debug=True)\n");
        fclose(file);
    }
    
    // Créer le template de base
    snprintf(file_path, sizeof(file_path), "%s/app/templates/base.html", project_path);
    file = fopen(file_path, "w");
    if (file) {
        // Utiliser fputs pour éviter les problèmes de format avec les templates Jinja2
        fputs("<!DOCTYPE html>\n", file);
        fputs("<html>\n", file);
        fputs("<head>\n", file);
        fputs("    <meta charset=\"utf-8\">\n", file);
        fputs("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n", file);
        fputs("    <title>{% block title %}Flask App{% endblock %}</title>\n", file);
        fputs("    <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/main.css') }}\">\n", file);
        fputs("</head>\n", file);
        fputs("<body>\n", file);
        fputs("    <header>\n", file);
        fputs("        <h1>Flask Application</h1>\n", file);
        fputs("    </header>\n", file);
        fputs("    <main>\n", file);
        fputs("        {% block content %}{% endblock %}\n", file);
        fputs("    </main>\n", file);
        fputs("    <footer>\n", file);
        fputs("        <p>&copy; 2023 Flask App</p>\n", file);
        fputs("    </footer>\n", file);
        fputs("    <script src=\"{{ url_for('static', filename='js/main.js') }}\"></script>\n", file);
        fputs("</body>\n", file);
        fputs("</html>\n", file);
        fclose(file);
    }
    
    // Créer le template index
    snprintf(file_path, sizeof(file_path), "%s/app/templates/index.html", project_path);
    file = fopen(file_path, "w");
    if (file) {
        // Utiliser fputs pour éviter les problèmes de format avec les templates Jinja2
        fputs("{% extends 'base.html' %}\n\n", file);
        fputs("{% block title %}Home - Flask App{% endblock %}\n\n", file);
        fputs("{% block content %}\n", file);
        fputs("<div class=\"container\">\n", file);
        fputs("    <h2>Welcome to your Flask Application</h2>\n", file);
        fputs("    <p>This is a starter template for a Flask web application.</p>\n", file);
        fputs("</div>\n", file);
        fputs("{% endblock %}\n", file);
        fclose(file);
    }
    
    // Créer le CSS principal
    snprintf(file_path, sizeof(file_path), "%s/app/static/css/main.css", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "* {\n");
        fprintf(file, "    box-sizing: border-box;\n");
        fprintf(file, "    margin: 0;\n");
        fprintf(file, "    padding: 0;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "body {\n");
        fprintf(file, "    font-family: Arial, sans-serif;\n");
        fprintf(file, "    line-height: 1.6;\n");
        fprintf(file, "    color: #333;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "header {\n");
        fprintf(file, "    background: #005f73;\n");
        fprintf(file, "    color: #fff;\n");
        fprintf(file, "    padding: 1rem;\n");
        fprintf(file, "    text-align: center;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "main {\n");
        fprintf(file, "    padding: 2rem;\n");
        fprintf(file, "}\n\n");
        fprintf(file, "footer {\n");
        fprintf(file, "    background: #333;\n");
        fprintf(file, "    color: #fff;\n");
        fprintf(file, "    text-align: center;\n");
        fprintf(file, "    padding: 1rem;\n");
        fprintf(file, "    position: fixed;\n");
        fprintf(file, "    bottom: 0;\n");
        fprintf(file, "    width: 100%%;\n");
        fprintf(file, "}\n\n");
        fprintf(file, ".container {\n");
        fprintf(file, "    max-width: 1200px;\n");
        fprintf(file, "    margin: 0 auto;\n");
        fprintf(file, "    overflow: auto;\n");
        fprintf(file, "    padding: 0 20px;\n");
        fprintf(file, "}\n");
        fclose(file);
    }
    
    // Créer le JS principal
    snprintf(file_path, sizeof(file_path), "%s/app/static/js/main.js", project_path);
    file = fopen(file_path, "w");
    if (file) {
        fprintf(file, "// Main JavaScript file\n");
        fprintf(file, "console.log('Flask app loaded');\n");
        fclose(file);
    }
}

int create_template_project(const char *project_name) {
    char backend_path[1024];
    char frontend_path[1024];
    
    // Create project directory
    if (create_directory_recursive(project_name) != 0) {
        return EXIT_FAILURE;
    }
    
    // Set up paths
    snprintf(backend_path, sizeof(backend_path), "%s/backend", project_name);
    snprintf(frontend_path, sizeof(frontend_path), "%s/frontend", project_name);
    
    // Create backend structure
    if (create_directory_recursive(backend_path) != 0) {
        return EXIT_FAILURE;
    }
    
    // Create frontend structure
    if (create_directory_recursive(frontend_path) != 0) {
        return EXIT_FAILURE;
    }
    
    // Create backend subdirectories
    for (int i = 0; template_backend[i] != NULL; i++) {
        char path[1024];
        snprintf(path, sizeof(path), "%s%s", backend_path, template_backend[i]);
        if (create_directory_recursive(path) != 0) {
            fprintf(stderr, "Error creating backend directory %s\n", path);
            // Continue with other directories
        }
    }
    
    // Create frontend subdirectories
    for (int i = 0; template_frontend[i] != NULL; i++) {
        char path[1024];
        snprintf(path, sizeof(path), "%s%s", frontend_path, template_frontend[i]);
        if (create_directory_recursive(path) != 0) {
            fprintf(stderr, "Error creating frontend directory %s\n", path);
            // Continue with other directories
        }
    }
    
    // Create template files
    create_backend_files(backend_path);
    create_frontend_files(frontend_path);
    
    printf("Successfully created project template: %s\n", project_name);
    return EXIT_SUCCESS;
}

// Créer des projets React et Flask
int create_project_by_type(const char *project_name, const char *project_type, const char *destination_path) {
    char full_project_path[MAX_PATH_LEN];
    char expanded_destination[MAX_PATH_LEN];
    
    // Expand tilde in destination path if present
    if (destination_path && destination_path[0] != '\0') {
        if (expand_tilde(destination_path, expanded_destination, sizeof(expanded_destination)) != 0) {
            fprintf(stderr, "Failed to expand path: %s\n", destination_path);
            return EXIT_FAILURE;
        }
        
        // Vérifier si le chemin de destination se termine par un slash
        if (expanded_destination[strlen(expanded_destination) - 1] == '/') {
            snprintf(full_project_path, sizeof(full_project_path), "%s%s", expanded_destination, project_name);
        } else {
            snprintf(full_project_path, sizeof(full_project_path), "%s/%s", expanded_destination, project_name);
        }
    } else {
        // Utiliser le répertoire courant
        snprintf(full_project_path, sizeof(full_project_path), "./%s", project_name);
    }
    
    // Créer le répertoire du projet
    if (create_directory_recursive(full_project_path) != 0) {
        fprintf(stderr, "Échec de la création du répertoire du projet: %s\n", full_project_path);
        return EXIT_FAILURE;
    }
    
    if (strcmp(project_type, "fullstack") == 0) {
        // Projet fullstack existant
        return create_template_project(full_project_path);
    } else if (strcmp(project_type, "react") == 0) {
        // Créer structure pour React
        for (int i = 0; template_react[i] != NULL; i++) {
            char path[MAX_PATH_LEN];
            snprintf(path, sizeof(path), "%s%s", full_project_path, template_react[i]);
            if (create_directory_recursive(path) != 0) {
                fprintf(stderr, "Erreur lors de la création du répertoire React %s\n", path);
                // Continuer avec les autres répertoires
            }
        }
        
        // Créer les fichiers React
        create_react_files(full_project_path);
        printf("Projet React créé avec succès: %s\n", full_project_path);
        return EXIT_SUCCESS;
    } else if (strcmp(project_type, "flask") == 0) {
        // Créer structure pour Flask
        for (int i = 0; template_flask[i] != NULL; i++) {
            char path[MAX_PATH_LEN];
            snprintf(path, sizeof(path), "%s%s", full_project_path, template_flask[i]);
            if (create_directory_recursive(path) != 0) {
                fprintf(stderr, "Erreur lors de la création du répertoire Flask %s\n", path);
                // Continuer avec les autres répertoires
            }
        }
        
        // Créer les fichiers Flask
        create_flask_files(full_project_path);
        printf("Projet Flask créé avec succès: %s\n", full_project_path);
        return EXIT_SUCCESS;
    } else {
        fprintf(stderr, "Type de projet non pris en charge: %s\n", project_type);
        fprintf(stderr, "Types de projets pris en charge: fullstack, react, flask\n");
        return EXIT_FAILURE;
    }
}

/**
 * Expands the tilde (~) in a path to the user's home directory
 * @param path The path that may contain a tilde
 * @param expanded_path The buffer to store the expanded path
 * @param size The size of the expanded_path buffer
 * @return 0 on success, -1 on failure
 */
int expand_tilde(const char *path, char *expanded_path, size_t size) {
    if (path == NULL || expanded_path == NULL) {
        return -1;
    }

    // Check if path starts with tilde
    if (path[0] == '~' && (path[1] == '/' || path[1] == '\0')) {
        const char *home = getenv("HOME");
        if (home == NULL) {
            // If HOME is not set, try to get it from passwd
            struct passwd *pw = getpwuid(getuid());
            if (pw == NULL) {
                return -1;
            }
            home = pw->pw_dir;
        }

        // Combine home directory with the rest of the path
        if (path[1] == '\0') {
            // Just "~"
            snprintf(expanded_path, size, "%s", home);
        } else {
            // "~/something"
            snprintf(expanded_path, size, "%s%s", home, path + 1);
        }
    } else {
        // No tilde, just copy the path
        strncpy(expanded_path, path, size);
        expanded_path[size - 1] = '\0';
    }

    return 0;
}

// Variables globales pour les modes
static int g_force_mode = 0;
static int g_verbose_mode = 0;
static int g_quiet_mode = 0;
static int g_home_directory_restriction = 1; // Restriction activée par défaut

// Variables globales pour la restriction des opérations au home directory
static char user_home_dir[4096] = {0};  // Using a fixed size instead of PATH_MAX

/**
 * Active la restriction des opérations au répertoire home
 */
void enable_home_directory_restriction() {
    g_home_directory_restriction = 1;
    printf("Sécurité activée : Opérations limitées au répertoire personnel de l'utilisateur\n");
}

/**
 * Désactive la restriction des opérations au répertoire home
 */
void disable_home_directory_restriction() {
    g_home_directory_restriction = 0;
    printf("ATTENTION : Sécurité désactivée. Les opérations peuvent être effectuées partout dans le système.\n");
    printf("Cette option peut être dangereuse et pourrait endommager votre système.\n");
}

/**
 * Vérifie si un chemin se trouve dans le répertoire home de l'utilisateur
 * 
 * @param path Le chemin à vérifier
 * @return 1 si le chemin est dans le home, 0 sinon
 */
int is_path_in_home_directory(const char *path) {
    if (!path || path[0] == '\0') {
        return 0;
    }

    // Obtenir le répertoire home de l'utilisateur
    const char *home = getenv("HOME");
    if (home == NULL) {
        // Si HOME n'est pas défini, essayer de l'obtenir via getpwuid
        struct passwd *pw = getpwuid(getuid());
        if (pw == NULL) {
            return 0;
        }
        home = pw->pw_dir;
    }

    // Si le chemin est absolu
    if (path[0] == '/') {
        // Vérifier si le chemin commence par le répertoire home
        size_t home_len = strlen(home);
        if (strncmp(path, home, home_len) == 0) {
            // S'assurer qu'après le home, il y a soit un slash, soit rien
            if (path[home_len] == '/' || path[home_len] == '\0') {
                return 1;
            }
        }
        return 0;
    } 
    // Si le chemin est relatif au home (~)
    else if (path[0] == '~' && (path[1] == '/' || path[1] == '\0')) {
        return 1;
    }
    // Si le chemin est relatif, il est considéré comme sûr car relatif au répertoire courant
    else {
        char cwd[MAX_PATH_LEN];
        if (getcwd(cwd, sizeof(cwd)) == NULL) {
            return 0; // En cas d'erreur, considérer comme non sûr
        }
        
        // Vérifier si le répertoire courant est dans le home
        size_t home_len = strlen(home);
        if (strncmp(cwd, home, home_len) == 0) {
            // S'assurer qu'après le home, il y a soit un slash, soit rien
            if (cwd[home_len] == '/' || cwd[home_len] == '\0') {
                return 1;
            }
        }
        return 0;
    }
}

/**
 * Vérifie si la restriction au répertoire home est activée
 */
int is_home_directory_restriction(void) {
    return g_home_directory_restriction;
}

/**
 * Set the force mode (overwrite existing files/directories)
 */
void set_force_mode(int mode) {
    g_force_mode = mode;
}

/**
 * Set the verbose mode (display detailed output)
 */
void set_verbose_mode(int mode) {
    g_verbose_mode = mode;
}

/**
 * Set the quiet mode (suppress all output)
 */
void set_quiet_mode(int mode) {
    g_quiet_mode = mode;
}

// Fonctions pour vérifier les modes
int is_force_mode(void) {
    return g_force_mode;
}

int is_verbose_mode(void) {
    return g_verbose_mode;
}

int is_quiet_mode(void) {
    return g_quiet_mode;
}

// Vérification si une chaîne est au format template (fichier:template)
int is_template_path(const char *path) {
    if (!path) return 0;
    
    // Vérifier si le chemin contient ":" mais pas au début (pour éviter les chemins Windows comme C:\...)
    const char *colon = strchr(path, ':');
    if (colon && colon != path) {
        // Vérifier qu'il y a du contenu après les deux côtés du :
        if (colon[1] != '\0' && colon != path) {
            return 1;
        }
    }
    
    return 0;
}

// Extraire l'information de destination et de template
int extract_template_info(const char *path, char *dest_path, char *template_path, size_t size) {
    if (!path || !dest_path || !template_path) return -1;
    
    // Trouver le séparateur ":"
    const char *colon = strchr(path, ':');
    if (!colon) return -1;
    
    // Calculer la longueur pour chaque partie
    size_t dest_len = colon - path;
    size_t template_len = strlen(colon + 1);
    
    // Vérifier si les longueurs sont valides et peuvent tenir dans les buffers
    if (dest_len == 0 || dest_len >= size || template_len == 0 || template_len >= size) {
        return -1;
    }
    
    // Copier les parties dans les buffers
    strncpy(dest_path, path, dest_len);
    dest_path[dest_len] = '\0'; // Assurez-vous que c'est bien terminé par un '\0'
    
    strncpy(template_path, colon + 1, size - 1);
    template_path[size - 1] = '\0'; // Assurez-vous que c'est bien terminé par un '\0'
    
    return 0;
}

// Créer un fichier à partir d'un template
int create_file_from_template(const char *dest_path, const char *template_path) {
    FILE *template_file, *dest_file;
    char buffer[4096];
    size_t read_size;
    
    // Vérifier si l'opération est limitée au répertoire home
    if (is_home_directory_restriction()) {
        if (!is_path_in_home_directory(dest_path)) {
            if (!is_quiet_mode()) {
                fprintf(stderr, "Erreur de sécurité: Le chemin de destination '%s' est en dehors de votre répertoire personnel.\n", dest_path);
                fprintf(stderr, "Les opérations sont restreintes à votre répertoire personnel pour des raisons de sécurité.\n");
            }
            return -1;
        }
        
        // Vérifier également le chemin du template
        if (!is_path_in_home_directory(template_path)) {
            if (!is_quiet_mode()) {
                fprintf(stderr, "Erreur de sécurité: Le chemin du template '%s' est en dehors de votre répertoire personnel.\n", template_path);
                fprintf(stderr, "Les opérations sont restreintes à votre répertoire personnel pour des raisons de sécurité.\n");
            }
            return -1;
        }
    }
    
    printf("Tentative de création de fichier à partir du template:\n");
    printf("- Destination: %s\n", dest_path);
    printf("- Template: %s\n", template_path);
    
    // Vérifier si le fichier destination existe déjà
    if (access(dest_path, F_OK) == 0 && !is_force_mode()) {
        if (!is_quiet_mode()) {
            fprintf(stderr, "Le fichier '%s' existe déjà. Utilisez -f pour forcer la réécriture.\n", dest_path);
        }
        return -1;
    }
    
    // Ouvrir le fichier template
    template_file = fopen(template_path, "rb");
    if (!template_file) {
        if (!is_quiet_mode()) {
            fprintf(stderr, "Impossible d'ouvrir le fichier template '%s': %s\n", template_path, strerror(errno));
        }
        return -1;
    }
    
    // Créer le répertoire parent si nécessaire
    char parent_dir[4096];
    strncpy(parent_dir, dest_path, sizeof(parent_dir) - 1);
    parent_dir[sizeof(parent_dir) - 1] = '\0';
    
    // Trouver le dernier séparateur de chemin
    char *last_slash = strrchr(parent_dir, '/');
    if (last_slash) {
        *last_slash = '\0'; // Terminer la chaîne là où commence le nom de fichier
        
        // Créer le répertoire parent si nécessaire
        if (strlen(parent_dir) > 0) {
            if (create_directory_recursive(parent_dir) != 0) {
                fclose(template_file);
                return -1;
            }
        }
    }
    
    // Ouvrir le fichier destination
    dest_file = fopen(dest_path, "wb");
    if (!dest_file) {
        if (!is_quiet_mode()) {
            fprintf(stderr, "Impossible de créer le fichier '%s': %s\n", dest_path, strerror(errno));
        }
        fclose(template_file);
        return -1;
    }
    
    printf("Copie du contenu du template vers la destination...\n");
    
    // Copier le contenu
    while ((read_size = fread(buffer, 1, sizeof(buffer), template_file)) > 0) {
        if (fwrite(buffer, 1, read_size, dest_file) != read_size) {
            if (!is_quiet_mode()) {
                fprintf(stderr, "Erreur lors de l'écriture dans '%s'\n", dest_path);
            }
            fclose(template_file);
            fclose(dest_file);
            return -1;
        }
    }
    
    // Fermer les fichiers
    fclose(template_file);
    fclose(dest_file);
    
    printf("Fichier créé avec succès à partir du template.\n");
    
    if (is_verbose_mode() && !is_quiet_mode()) {
        printf("Fichier créé à partir du template: %s (Source: %s)\n", dest_path, template_path);
    }
    
    return 0;
}

int create_file_with_content(const char *filepath, const char *content) {
    // Vérifier que le chemin et le contenu ne sont pas NULL
    if (!filepath) {
        fprintf(stderr, "Error: NULL filepath provided\n");
        return -1;
    }

    // Vérifier si l'opération est limitée au répertoire home
    if (is_home_directory_restriction()) {
        if (!is_path_in_home_directory(filepath)) {
            if (!is_quiet_mode()) {
                fprintf(stderr, "Erreur de sécurité: Le chemin '%s' est en dehors de votre répertoire personnel.\n", filepath);
                fprintf(stderr, "Les opérations sont restreintes à votre répertoire personnel pour des raisons de sécurité.\n");
            }
            return -1;
        }
    }

    // Créer les répertoires parents si nécessaire
    char *dir_path = strdup(filepath);
    if (!dir_path) {
        perror("Failed to allocate memory for directory path");
        return -1;
    }

    // Trouver le dernier séparateur de chemin pour isoler le chemin du répertoire
    char *last_slash = strrchr(dir_path, '/');
    if (last_slash) {
        *last_slash = '\0'; // Terminer la chaîne au dernier slash
        if (strlen(dir_path) > 0) {
            if (create_directory_recursive(dir_path) != 0) {
                free(dir_path);
                return -1;
            }
        }
    }
    free(dir_path);

    // Créer ou tronquer le fichier
    FILE *file = fopen(filepath, "w");
    if (!file) {
        fprintf(stderr, "Failed to create file '%s': %s\n", filepath, strerror(errno));
        return -1;
    }

    // Écrire le contenu si fourni
    if (content && fputs(content, file) == EOF) {
        fprintf(stderr, "Failed to write content to file '%s': %s\n", filepath, strerror(errno));
        fclose(file);
        return -1;
    }

    fclose(file);
    return 0;
}