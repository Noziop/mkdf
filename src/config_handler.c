#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <pwd.h>
#include "../include/config_handler.h"

// Configuration globale 
static mkdf_config_t global_config;
static int config_initialized = 0;

// Fonction pour récupérer le chemin du répertoire home de l'utilisateur
static int get_home_dir(char *buffer, size_t size) {
    const char *homedir;
    
    // D'abord essayer la variable d'environnement HOME
    homedir = getenv("HOME");
    if (homedir == NULL) {
        // Si HOME n'est pas défini, utiliser getpwuid
        struct passwd *pw = getpwuid(getuid());
        if (pw == NULL) {
            fprintf(stderr, "Erreur: Impossible de déterminer le répertoire home de l'utilisateur\n");
            return -1;
        }
        homedir = pw->pw_dir;
    }
    
    // Vérifier que le buffer est assez grand
    if (strlen(homedir) + 20 >= size) {
        fprintf(stderr, "Erreur: Buffer trop petit pour le chemin du répertoire home\n");
        return -1;
    }
    
    strncpy(buffer, homedir, size - 1);
    buffer[size - 1] = '\0';
    return 0;
}

int get_config_file_path(char *buffer, size_t size) {
    char home_dir[4096];
    
    // Récupérer le répertoire home
    if (get_home_dir(home_dir, sizeof(home_dir)) != 0) {
        return -1;
    }
    
    // Construire le chemin complet du fichier de configuration
    snprintf(buffer, size, "%s/.config/mkdf/config", home_dir);
    return 0;
}

// Crée les répertoires nécessaires pour le fichier de configuration
static int create_config_directories(const char *config_path) {
    char dir_path[4096];
    char *last_slash = strrchr(config_path, '/');
    
    if (last_slash == NULL) {
        fprintf(stderr, "Erreur: Chemin de configuration invalide\n");
        return -1;
    }
    
    // Copier le chemin jusqu'au dernier slash
    size_t dir_len = last_slash - config_path;
    if (dir_len >= sizeof(dir_path)) {
        fprintf(stderr, "Erreur: Chemin trop long\n");
        return -1;
    }
    
    strncpy(dir_path, config_path, dir_len);
    dir_path[dir_len] = '\0';
    
    // Créer les répertoires récursivement
    char temp_path[4096];
    char *p = dir_path;
    
    // Ignorer le premier caractère s'il s'agit d'un slash
    if (*p == '/') p++;
    
    while (*p) {
        // Trouver le prochain slash
        char *next_slash = strchr(p, '/');
        if (next_slash) {
            strncpy(temp_path, dir_path, next_slash - dir_path);
            temp_path[next_slash - dir_path] = '\0';
            
            // Créer le répertoire si nécessaire
            struct stat st;
            if (stat(temp_path, &st) != 0) {
                if (mkdir(temp_path, 0755) != 0 && errno != EEXIST) {
                    perror("Erreur lors de la création du répertoire");
                    return -1;
                }
            }
            
            p = next_slash + 1;
        } else {
            // Dernier composant
            if (mkdir(dir_path, 0755) != 0 && errno != EEXIST) {
                perror("Erreur lors de la création du répertoire");
                return -1;
            }
            break;
        }
    }
    
    return 0;
}

// Détermine le chemin d'installation par défaut pour le web root
static int determine_default_web_root(char *buffer, size_t size) {
    // D'abord vérifier la variable d'environnement
    const char *env_path = getenv("MKDF_WEB_ROOT");
    if (env_path) {
        strncpy(buffer, env_path, size - 1);
        buffer[size - 1] = '\0';
        return 0;
    }
    
    // Essayer de trouver le chemin relatif à l'exécutable
    char exe_path[4096] = {0};
    ssize_t len = readlink("/proc/self/exe", exe_path, sizeof(exe_path) - 1);
    if (len != -1) {
        exe_path[len] = '\0';
        
        // Trouver le dernier slash pour isoler le répertoire de l'exécutable
        char *last_slash = strrchr(exe_path, '/');
        if (last_slash) {
            *last_slash = '\0'; // Tronquer au dernier slash
            
            // Vérifier les chemins possibles pour le répertoire web
            struct stat st;
            char test_path[4096];
            
            // 1. Répertoire web dans le même répertoire que l'exécutable
            snprintf(test_path, sizeof(test_path), "%s/web", exe_path);
            if (stat(test_path, &st) == 0 && S_ISDIR(st.st_mode)) {
                strncpy(buffer, test_path, size - 1);
                buffer[size - 1] = '\0';
                return 0;
            }
            
            // 2. Répertoire web un niveau au-dessus
            snprintf(test_path, sizeof(test_path), "%s/../web", exe_path);
            if (stat(test_path, &st) == 0 && S_ISDIR(st.st_mode)) {
                // Convertir le chemin relatif en chemin absolu
                char resolved_path[4096];
                if (realpath(test_path, resolved_path) != NULL) {
                    strncpy(buffer, resolved_path, size - 1);
                    buffer[size - 1] = '\0';
                    return 0;
                }
            }
            
            // 3. Si l'exécutable est dans /usr/bin ou /usr/local/bin,
            // essayer /usr/share/mkdf/web ou /usr/local/share/mkdf/web
            if (strcmp(exe_path, "/usr/bin") == 0) {
                snprintf(buffer, size, "/usr/share/mkdf/web");
                return 0;
            } else if (strcmp(exe_path, "/usr/local/bin") == 0) {
                snprintf(buffer, size, "/usr/local/share/mkdf/web");
                return 0;
            }
        }
    }
    
    // Si tout échoue, utiliser le répertoire courant
    snprintf(buffer, size, "./web");
    return 0;
}

// Détermine le chemin par défaut pour les templates
static int determine_default_template_dir(char *buffer, size_t size) {
    // Logique similaire à celle du web root
    char web_root[4096];
    determine_default_web_root(web_root, sizeof(web_root));
    
    // Si web_root se termine par "/web", remplacer par "/templates"
    char *web_suffix = strstr(web_root, "/web");
    if (web_suffix && strcmp(web_suffix, "/web") == 0) {
        // Calculer la taille du préfixe (avant "/web")
        size_t prefix_size = web_suffix - web_root;
        if (prefix_size + 11 < size) { // +11 pour "/templates" + '\0'
            strncpy(buffer, web_root, prefix_size);
            strcpy(buffer + prefix_size, "/templates");
            return 0;
        }
    }
    
    // Fallback: utiliser le même répertoire que web_root mais avec "/templates" à la place de "/web"
    char *last_slash = strrchr(web_root, '/');
    if (last_slash) {
        size_t prefix_size = last_slash - web_root;
        if (prefix_size + 11 < size) {
            strncpy(buffer, web_root, prefix_size);
            strcpy(buffer + prefix_size, "/templates");
            return 0;
        }
    }
    
    // Si tout échoue, utiliser le répertoire courant
    snprintf(buffer, size, "./templates");
    return 0;
}

int create_default_config(void) {
    char config_path[4096];
    mkdf_config_t config;
    
    // Obtenir le chemin du fichier de configuration
    if (get_config_file_path(config_path, sizeof(config_path)) != 0) {
        return -1;
    }
    
    // Créer les répertoires nécessaires
    if (create_config_directories(config_path) != 0) {
        return -1;
    }
    
    // Initialiser la configuration par défaut
    determine_default_web_root(config.web_root_path, sizeof(config.web_root_path));
    config.web_port = 8080; // Port par défaut
    config.debug_mode = 0;  // Mode debug désactivé par défaut
    determine_default_template_dir(config.template_dir, sizeof(config.template_dir));
    strncpy(config.locale, "fr_FR", sizeof(config.locale) - 1);
    
    // Sauvegarder la configuration
    return save_config(&config);
}

int save_config(const mkdf_config_t *config) {
    char config_path[4096];
    
    // Obtenir le chemin du fichier de configuration
    if (get_config_file_path(config_path, sizeof(config_path)) != 0) {
        return -1;
    }
    
    // Créer les répertoires nécessaires s'ils n'existent pas
    if (create_config_directories(config_path) != 0) {
        return -1;
    }
    
    // Ouvrir le fichier en écriture
    FILE *file = fopen(config_path, "w");
    if (!file) {
        perror("Erreur lors de l'ouverture du fichier de configuration");
        return -1;
    }
    
    // Écrire les paramètres de configuration
    fprintf(file, "# Configuration de MKDF\n");
    fprintf(file, "# Généré automatiquement\n\n");
    
    fprintf(file, "# Chemin vers les fichiers web\n");
    fprintf(file, "WEB_ROOT_PATH=%s\n\n", config->web_root_path);
    
    fprintf(file, "# Port du serveur web\n");
    fprintf(file, "WEB_PORT=%d\n\n", config->web_port);
    
    fprintf(file, "# Mode debug (0=désactivé, 1=activé)\n");
    fprintf(file, "DEBUG_MODE=%d\n\n", config->debug_mode);
    
    fprintf(file, "# Répertoire des templates\n");
    fprintf(file, "TEMPLATE_DIR=%s\n\n", config->template_dir);
    
    fprintf(file, "# Paramètre régional\n");
    fprintf(file, "LOCALE=%s\n", config->locale);
    
    fclose(file);
    printf("Configuration sauvegardée dans %s\n", config_path);
    return 0;
}

// Fonction pour analyser une ligne de configuration
static void parse_config_line(char *line, mkdf_config_t *config) {
    // Ignorer les commentaires et les lignes vides
    if (line[0] == '#' || line[0] == '\0' || line[0] == '\n')
        return;
    
    // Trouver le signe égal
    char *equal_sign = strchr(line, '=');
    if (!equal_sign)
        return;
    
    // Séparer la clé et la valeur
    *equal_sign = '\0';
    char *key = line;
    char *value = equal_sign + 1;
    
    // Supprimer les espaces et les sauts de ligne
    char *p = value + strlen(value) - 1;
    while (p >= value && (*p == ' ' || *p == '\n' || *p == '\r'))
        *p-- = '\0';
    
    // Vérifier la clé et définir la valeur correspondante
    if (strcmp(key, "WEB_ROOT_PATH") == 0 || strcmp(key, "WEB_ROOT") == 0) {
        strncpy(config->web_root_path, value, sizeof(config->web_root_path) - 1);
        config->web_root_path[sizeof(config->web_root_path) - 1] = '\0';
    } else if (strcmp(key, "WEB_PORT") == 0) {
        config->web_port = atoi(value);
    } else if (strcmp(key, "DEBUG_MODE") == 0) {
        config->debug_mode = atoi(value);
    } else if (strcmp(key, "TEMPLATE_DIR") == 0) {
        strncpy(config->template_dir, value, sizeof(config->template_dir) - 1);
        config->template_dir[sizeof(config->template_dir) - 1] = '\0';
    } else if (strcmp(key, "LOCALE") == 0) {
        strncpy(config->locale, value, sizeof(config->locale) - 1);
        config->locale[sizeof(config->locale) - 1] = '\0';
    }
}

mkdf_config_t load_config(void) {
    char config_path[4096];
    mkdf_config_t config;
    char line[4096];
    
    // Initialiser config avec des valeurs par défaut au cas où certaines options ne seraient pas définies dans le fichier
    determine_default_web_root(config.web_root_path, sizeof(config.web_root_path));
    config.web_port = 8080;
    config.debug_mode = 0;
    determine_default_template_dir(config.template_dir, sizeof(config.template_dir));
    strncpy(config.locale, "fr_FR", sizeof(config.locale) - 1);
    
    // Obtenir le chemin du fichier de configuration
    if (get_config_file_path(config_path, sizeof(config_path)) != 0) {
        fprintf(stderr, "Impossible d'obtenir le chemin du fichier de configuration. Utilisation des valeurs par défaut.\n");
        return config;
    }
    
    // Vérifier si le fichier existe
    FILE *file = fopen(config_path, "r");
    if (!file) {
        // Si le fichier n'existe pas, créer un fichier de configuration par défaut
        if (errno == ENOENT) {
            if (create_default_config() == 0) {
                // Réessayer d'ouvrir le fichier après sa création
                file = fopen(config_path, "r");
                if (!file) {
                    fprintf(stderr, "Erreur lors de l'ouverture du fichier de configuration après sa création. Utilisation des valeurs par défaut.\n");
                    return config;
                }
            } else {
                fprintf(stderr, "Erreur lors de la création du fichier de configuration. Utilisation des valeurs par défaut.\n");
                return config;
            }
        } else {
            perror("Erreur lors de l'ouverture du fichier de configuration");
            return config;
        }
    }
    
    // Lire et analyser le fichier ligne par ligne
    while (fgets(line, sizeof(line), file)) {
        parse_config_line(line, &config);
    }
    
    fclose(file);
    return config;
}

mkdf_config_t *get_global_config(void) {
    // Si la configuration n'a pas encore été initialisée, le faire
    if (!config_initialized) {
        init_config();
    }
    
    return &global_config;
}

int init_config(void) {
    if (!config_initialized) {
        global_config = load_config();
        config_initialized = 1;
    }
    
    return 0;
}