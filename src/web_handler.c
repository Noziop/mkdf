#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <dirent.h>
#include <signal.h>
#include <errno.h>
#include <libgen.h> /* Pour basename() */
#include "../include/web_handler.h"
#include "../include/directory_handler.h"

#define PORT 8080
#define BUFFER_SIZE 8192
#define MAX_PATH_LEN 4096
#define WEB_ROOT "/home/noziop/projects/mkdf/web"
#define PID_FILE "/tmp/mkdf_web_server.pid"

// Forward declarations of functions
static int create_project_from_template(const char *path, const char *template_type);
static char* explore_directory(const char *path);
static void build_directory_tree(const char *path, char *output, size_t output_size, int level, size_t *current_size);

// Global variables for web server communication
int web_pipe[2];
pid_t web_server_pid;

// Structure to pass to the handler thread
typedef struct {
    int client_fd;
} thread_args_t;

// Signal handler for graceful termination
static void handle_signal(int sig) {
    if (sig == SIGINT || sig == SIGTERM) {
        printf("\nReceived signal %d. Shutting down web server...\n", sig);
        // Delete PID file before exiting
        unlink(PID_FILE);
        exit(0);
    }
}

// Function to save the PID of the web server to a file
static int save_pid_to_file(pid_t pid) {
    FILE *f = fopen(PID_FILE, "w");
    if (!f) {
        perror("Failed to open PID file for writing");
        return -1;
    }
    
    fprintf(f, "%d", pid);
    fclose(f);
    return 0;
}

// Function to read the PID of the web server from the file
static pid_t read_pid_from_file(void) {
    FILE *f = fopen(PID_FILE, "r");
    if (!f) {
        // If file doesn't exist, server is not running
        return -1;
    }
    
    pid_t pid;
    if (fscanf(f, "%d", &pid) != 1) {
        fclose(f);
        return -1;
    }
    
    fclose(f);
    return pid;
}

// Function to read the index.html file from the web folder
static char* read_html_template() {
    char file_path[MAX_PATH_LEN];
    snprintf(file_path, sizeof(file_path), "%s/index.html", WEB_ROOT);
    
    // Open the file
    FILE *file = fopen(file_path, "r");
    if (!file) {
        perror("Failed to open index.html");
        return NULL;
    }
    
    // Get file size
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    rewind(file);
    
    // Allocate memory for the file content
    char *buffer = malloc(file_size + 1);
    if (!buffer) {
        perror("Failed to allocate memory for HTML template");
        fclose(file);
        return NULL;
    }
    
    // Read the file
    size_t read_size = fread(buffer, 1, file_size, file);
    buffer[read_size] = '\0';
    
    fclose(file);
    return buffer;
}

// Function to read a CSS file from the web folder
static char* read_css_file(const char *css_path) {
    char file_path[MAX_PATH_LEN];
    snprintf(file_path, sizeof(file_path), "%s/%s", WEB_ROOT, css_path);
    
    // Open the file
    FILE *file = fopen(file_path, "r");
    if (!file) {
        perror("Failed to open CSS file");
        return NULL;
    }
    
    // Get file size
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    rewind(file);
    
    // Allocate memory for the file content
    char *buffer = malloc(file_size + 1);
    if (!buffer) {
        perror("Failed to allocate memory for CSS content");
        fclose(file);
        return NULL;
    }
    
    // Read the file
    size_t read_size = fread(buffer, 1, file_size, file);
    buffer[read_size] = '\0';
    
    fclose(file);
    return buffer;
}

// Function to handle HTTP requests
void *handle_client(void *arg) {
    thread_args_t *args = (thread_args_t *)arg;
    int client_fd = args->client_fd;
    
    // Allouer des buffers suffisamment grands sur le tas au lieu de la pile
    // Augmenter la taille du buffer de réponse pour éviter les débordements
    char *buffer = malloc(BUFFER_SIZE * 2); // Double la taille du buffer pour plus de sécurité
    char *response = malloc(BUFFER_SIZE * 4); // Quadruple la taille pour la réponse
    
    if (!buffer || !response) {
        perror("malloc failed in handle_client");
        if (buffer) free(buffer);
        if (response) free(response);
        close(client_fd);
        free(args);
        return NULL;
    }
    
    // Initialiser les buffers à zéro
    memset(buffer, 0, BUFFER_SIZE * 2);
    memset(response, 0, BUFFER_SIZE * 4);
    
    // Lire la requête avec une limite pour éviter les débordements
    ssize_t bytes_read = read(client_fd, buffer, BUFFER_SIZE * 2 - 1);
    if (bytes_read <= 0) {
        close(client_fd);
        free(buffer);
        free(response);
        free(args);
        return NULL;
    }
    
    // S'assurer que le buffer est bien terminé par un caractère nul
    buffer[bytes_read] = '\0';
    
    // Traiter la requête de manière sécurisée
    handle_web_request(buffer, response);
    
    // Envoyer la réponse
    size_t response_len = strlen(response);
    ssize_t bytes_sent = 0;
    ssize_t total_sent = 0;
    
    // Envoyer par morceaux pour éviter les problèmes avec les grandes réponses
    while (total_sent < response_len) {
        bytes_sent = write(client_fd, response + total_sent, response_len - total_sent);
        if (bytes_sent <= 0) {
            // Erreur d'écriture
            break;
        }
        total_sent += bytes_sent;
    }
    
    // Nettoyer
    close(client_fd);
    free(buffer);
    free(response);
    free(args);
    return NULL;
}

// Parse HTTP request to extract parameters
static void parse_request(const char *request, char *method, char *path, char *content) {
    // Initialize output
    method[0] = '\0';
    path[0] = '\0';
    content[0] = '\0';
    
    // Extract method and path
    if (sscanf(request, "%s %s", method, path) < 2) {
        return;
    }
    
    // If it's a POST request, extract content
    if (strcmp(method, "POST") == 0) {
        const char *body = strstr(request, "\r\n\r\n");
        if (body) {
            body += 4; // Skip "\r\n\r\n"
            strcpy(content, body);
        }
    }
}

// Extract parameter value from URL-encoded content
static void extract_param(const char *content, const char *param_name, char *value, size_t value_size) {
    char search_param[256];
    snprintf(search_param, sizeof(search_param), "%s=", param_name);
    
    const char *param_start = strstr(content, search_param);
    if (param_start) {
        param_start += strlen(search_param);
        const char *param_end = strchr(param_start, '&');
        
        if (param_end) {
            // Parameter is followed by other parameters
            size_t len = param_end - param_start;
            if (len < value_size) {
                strncpy(value, param_start, len);
                value[len] = '\0';
            } else {
                strncpy(value, param_start, value_size - 1);
                value[value_size - 1] = '\0';
            }
        } else {
            // Parameter is the last or only one
            strncpy(value, param_start, value_size - 1);
            value[value_size - 1] = '\0';
        }
        
        // URL decode the value
        char *src = value;
        char *dst = value;
        while (*src) {
            if (*src == '%' && src[1] && src[2]) {
                char hex[3] = {src[1], src[2], '\0'};
                *dst = (char)strtol(hex, NULL, 16);
                src += 3;
                dst++;
            } else if (*src == '+') {
                *dst = ' ';
                src++;
                dst++;
            } else {
                *dst = *src;
                src++;
                dst++;
            }
        }
        *dst = '\0';
    } else {
        value[0] = '\0';
    }
}

// handle_web_request: Utilisation plus sécurisée des tampons pour éviter le stack smashing
int handle_web_request(const char *request, char *response) {
    char method[16] = {0}, path[256] = {0}, content[BUFFER_SIZE] = {0};
    parse_request(request, method, path, content);
    
    // Définir la taille maximale du tampon de réponse (BUFFER_SIZE * 4 dans handle_client)
    const size_t response_buffer_size = BUFFER_SIZE * 4;
    
    // Handle GET request for the main page or HTML files
    if (strcmp(method, "GET") == 0 && (strcmp(path, "/") == 0 || strcmp(path, "/index.html") == 0)) {
        char *html_template = read_html_template();
        if (html_template) {
            size_t html_len = strlen(html_template);
            
            // Vérifier que le contenu n'est pas trop grand pour le tampon
            if (html_len > response_buffer_size - 200) {
                // Tronquer le contenu HTML si nécessaire
                html_template[response_buffer_size - 200] = '\0';
                html_len = response_buffer_size - 200;
            }
            
            snprintf(response, response_buffer_size, 
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s", 
                html_len, html_template);
            free(html_template);
        } else {
            const char *error_msg = "Failed to load HTML template";
            snprintf(response, response_buffer_size, 
                "HTTP/1.1 500 Internal Server Error\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s", 
                strlen(error_msg), error_msg);
        }
        return 0;
    }
    
    // Handle GET request for CSS files
    if (strcmp(method, "GET") == 0) {
        const char *css_ext = ".css";
        size_t css_ext_len = strlen(css_ext);
        size_t path_len = strlen(path);
        
        // Check if path ends with .css
        if (path_len > css_ext_len && strcmp(path + path_len - css_ext_len, css_ext) == 0) {
            // Remove leading slash from path
            const char *css_path = (*path == '/') ? path + 1 : path;
            
            char *css_content = read_css_file(css_path);
            if (css_content) {
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/css\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(css_content), css_content);
                free(css_content);
                return 0;
            }
        }
    }
    
    // Handle POST request to create template project
    if (strcmp(method, "POST") == 0 && strcmp(path, "/create_template") == 0) {
        char project_path[MAX_PATH_LEN] = {0};
        extract_param(content, "path", project_path, sizeof(project_path));
        
        if (strlen(project_path) > 0) {
            int result = create_template_project(project_path);
            
            if (result == EXIT_SUCCESS) {
                // Utiliser un buffer plus grand pour éviter le débordement
                char success_msg[2048];
                
                // Assurez-vous que le message ne dépasse pas la taille du buffer
                if (strlen(project_path) > 1500) {
                    // Tronquer le chemin du projet s'il est trop long
                    char truncated_path[500];
                    strncpy(truncated_path, project_path, 496);
                    truncated_path[496] = '\0';
                    strcat(truncated_path, "...");
                    snprintf(success_msg, sizeof(success_msg), "Project successfully created at: %s", truncated_path);
                } else {
                    snprintf(success_msg, sizeof(success_msg), "Project successfully created at: %s", project_path);
                }
                
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(success_msg), success_msg);
            } else {
                const char *error_msg = "Failed to create project. Please check the path and permissions.";
                
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 400 Bad Request\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(error_msg), error_msg);
            }
        } else {
            const char *error_msg = "Invalid project path";
            
            snprintf(response, response_buffer_size, 
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s", 
                strlen(error_msg), error_msg);
        }
        
        return 0;
    }
    
    // Handle POST request to create custom structure
    if (strcmp(method, "POST") == 0 && strcmp(path, "/create_custom") == 0) {
        char structure[MAX_PATH_LEN] = {0};
        extract_param(content, "structure", structure, sizeof(structure));
        
        if (strlen(structure) > 0) {
            int result = create_directory_structure(structure);
            
            if (result == EXIT_SUCCESS) {
                // Utiliser un buffer sécurisé pour le message
                char success_msg[2048];
                
                // Créer un message de succès approprié sans risquer de débordement
                if (strlen(structure) > 100) {
                    snprintf(success_msg, sizeof(success_msg), 
                        "Successfully created directory structure from pattern: %.50s... (truncated)",
                        structure);
                } else {
                    snprintf(success_msg, sizeof(success_msg), 
                        "Successfully created directory structure from pattern: %s",
                        structure);
                }
                
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(success_msg), success_msg);
            } else {
                const char *error_msg = "Failed to create directory structure. Please check the pattern and path permissions.";
                
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 400 Bad Request\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(error_msg), error_msg);
            }
        } else {
            const char *error_msg = "Invalid structure pattern";
            
            snprintf(response, response_buffer_size, 
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s", 
                strlen(error_msg), error_msg);
        }
        
        return 0;
    }
    
    // Nouvel endpoint pour créer un projet à partir d'un modèle spécifique
    if (strcmp(method, "POST") == 0 && strcmp(path, "/create_template_project") == 0) {
        char project_path[MAX_PATH_LEN] = {0};
        char template_type[32] = {0};
        
        extract_param(content, "path", project_path, sizeof(project_path));
        extract_param(content, "template", template_type, sizeof(template_type));
        
        if (strlen(project_path) > 0 && strlen(template_type) > 0) {
            int result = create_project_from_template(project_path, template_type);
            
            if (result == EXIT_SUCCESS) {
                // Utiliser un buffer plus grand pour éviter le débordement
                char success_msg[2048];
                
                // Assurez-vous que le message ne dépasse pas la taille du buffer
                snprintf(success_msg, sizeof(success_msg), 
                    "Projet '%s' créé avec succès à l'emplacement: %s", 
                    template_type, project_path);
                
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(success_msg), success_msg);
            } else {
                const char *error_msg = "Échec de création du projet. Veuillez vérifier le chemin et les permissions.";
                
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 400 Bad Request\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(error_msg), error_msg);
            }
        } else {
            const char *error_msg = "Chemin de projet ou type de modèle invalide";
            
            snprintf(response, response_buffer_size, 
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s", 
                strlen(error_msg), error_msg);
        }
        
        return 0;
    }
    
    // Nouvel endpoint pour explorer un répertoire
    if (strcmp(method, "POST") == 0 && strcmp(path, "/explore_directory") == 0) {
        char dir_path[MAX_PATH_LEN] = {0};
        extract_param(content, "path", dir_path, sizeof(dir_path));
        
        if (strlen(dir_path) > 0) {
            char *directory_structure = explore_directory(dir_path);
            
            if (directory_structure) {
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(directory_structure), directory_structure);
                
                free(directory_structure);
            } else {
                const char *error_msg = "Erreur lors de l'exploration du répertoire";
                
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 500 Internal Server Error\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(error_msg), error_msg);
            }
        } else {
            const char *error_msg = "Chemin de répertoire invalide";
            
            snprintf(response, response_buffer_size, 
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s", 
                strlen(error_msg), error_msg);
        }
        
        return 0;
    }
    
    // Nouvel endpoint pour lister le contenu d'un répertoire pour l'explorateur de fichiers
    if (strcmp(method, "POST") == 0 && strcmp(path, "/list_directory") == 0) {
        char dir_path[MAX_PATH_LEN] = {0};
        extract_param(content, "path", dir_path, sizeof(dir_path));
        
        if (strlen(dir_path) > 0) {
            // Buffer pour stocker la réponse JSON
            char json_response[BUFFER_SIZE] = {0};
            
            // Lister le contenu du répertoire
            int result = list_directory(dir_path, json_response);
            
            if (result == 0) {
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(json_response), json_response);
            } else {
                snprintf(response, response_buffer_size, 
                    "HTTP/1.1 500 Internal Server Error\r\n"
                    "Content-Type: application/json\r\n"
                    "Content-Length: %zu\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "%s", 
                    strlen(json_response), json_response);
            }
        } else {
            const char *error_msg = "{\"error\": \"Chemin de répertoire invalide\"}";
            
            snprintf(response, response_buffer_size, 
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: application/json\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s", 
                strlen(error_msg), error_msg);
        }
        
        return 0;
    }
    
    // Handle 404 Not Found
    const char *not_found = "404 Not Found";
    snprintf(response, response_buffer_size, 
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: %zu\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s", 
        strlen(not_found), not_found);
    
    return 0;
}

// Fonction pour créer un projet basé sur un modèle spécifique
static int create_project_from_template(const char *path, const char *template_type) {
    char structure[MAX_PATH_LEN];

    // Sélection du modèle basé sur le type
    if (strcmp(template_type, "simple") == 0) {
        snprintf(structure, sizeof(structure), "%s/{src/,docs/,README.md}", path);
    }
    else if (strcmp(template_type, "multi") == 0) {
        snprintf(structure, sizeof(structure), 
                "%s/{src/{lib/,bin/,include/},docs/{user/,dev/},tests/,README.md,LICENSE}", path);
    }
    else if (strcmp(template_type, "docker") == 0) {
        snprintf(structure, sizeof(structure), 
                "%s/{src/,docker/{app/Dockerfile,nginx/{Dockerfile,nginx.conf},docker-compose.yml},README.md}", path);
    }
    else if (strcmp(template_type, "fastapi") == 0) {
        snprintf(structure, sizeof(structure), 
                "%s/{app/{api/{v1/endpoints/{users.py,items.py},__init__.py},core/{config.py,__init__.py},db/{models/,session.py,__init__.py},main.py,__init__.py},tests/,requirements.txt,README.md}", path);
    }
    else if (strcmp(template_type, "vuevite") == 0) {
        snprintf(structure, sizeof(structure), 
                "%s/{public/{favicon.ico,robots.txt},src/{assets/,components/HelloWorld.vue,views/{HomeView.vue,AboutView.vue},App.vue,main.js,router.js},package.json,vite.config.js,README.md}", path);
    }
    else if (strcmp(template_type, "react") == 0) {
        snprintf(structure, sizeof(structure), 
                "%s/{public/{favicon.ico,robots.txt,index.html},src/{components/{App.js,Header.js,Footer.js},pages/{Home.js,About.js},assets/images/,styles/,App.css,index.css,index.js},package.json,.gitignore,README.md}", path);
    }
    else if (strcmp(template_type, "flask") == 0) {
        snprintf(structure, sizeof(structure), 
                "%s/{app/{static/{css/,js/,images/},templates/{base.html,index.html,about.html},__init__.py,routes.py,models.py,forms.py},tests/,migrations/,config.py,requirements.txt,run.py,README.md}", path);
    }
    else {
        // Si le type de modèle n'est pas reconnu, utiliser le modèle simple par défaut
        snprintf(structure, sizeof(structure), "%s/{src/,docs/,README.md}", path);
    }

    // Créer la structure du projet
    return create_directory_structure(structure);
}

// Fonction pour déterminer si un répertoire doit être filtré
static int should_filter_directory(const char *dirname) {
    // Liste des répertoires à filtrer
    const char *filtered_dirs[] = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        ".idea",
        ".vscode",
        ".cache",
        ".npm",
        "dist",
        "build",
        ".next",
        "out",
        ".nuxt",
        ".sass-cache",
        ".pytest_cache",
        "__snapshots__",
        "coverage",
        ".nyc_output",
        NULL  // Marque la fin de la liste
    };
    
    // Vérification si le répertoire est dans la liste des filtres
    for (int i = 0; filtered_dirs[i] != NULL; i++) {
        if (strcmp(dirname, filtered_dirs[i]) == 0) {
            return 1; // Doit être filtré
        }
    }
    
    return 0; // Ne doit pas être filtré
}

// Réécriture complète de la fonction pour éviter les problèmes de débordement de pile
static void build_directory_tree(const char *path, char *output, size_t output_size, int level, size_t *current_size) {
    DIR *dir;
    struct dirent *entry;
    struct stat statbuf;
    char full_path[MAX_PATH_LEN];
    
    // Vérification de sécurité pour l'espace restant dans le buffer
    // Nous gardons au moins 200 octets comme marge de sécurité
    if (*current_size >= output_size - 200) {
        size_t safe_space = output_size - *current_size - 1;
        if (safe_space > 40) {
            snprintf(output + *current_size, safe_space, "\n... (sortie tronquée, trop de fichiers) ...");
            *current_size += strlen(output + *current_size);
        }
        return;
    }
    
    // Ouverture du répertoire
    if (!(dir = opendir(path))) {
        size_t safe_space = output_size - *current_size - 1;
        if (safe_space > 50) {
            int bytes_added = snprintf(output + *current_size, safe_space, 
                                     "\nErreur: Impossible d'ouvrir le répertoire %s\n", path);
            if (bytes_added > 0) {
                *current_size += bytes_added;
            }
        }
        return;
    }
    
    // Traitement des entrées du répertoire
    while ((entry = readdir(dir)) != NULL) {
        // Vérification de sécurité pour l'espace restant
        if (*current_size >= output_size - 200) {
            size_t safe_space = output_size - *current_size - 1;
            if (safe_space > 40) {
                int bytes_added = snprintf(output + *current_size, safe_space,
                                         "\n... (sortie tronquée, trop de fichiers) ...");
                if (bytes_added > 0) {
                    *current_size += bytes_added;
                }
            }
            break;
        }
        
        // Ignorer . et ..
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;
            
        // Ignorer les répertoires qui sont dans la liste de filtrage
        if (should_filter_directory(entry->d_name))
            continue;
        
        // Construction du chemin complet avec vérification de taille
        if (snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name) >= sizeof(full_path)) {
            // Chemin trop long, ignorer cette entrée
            continue;
        }
        
        // Obtention des informations sur le fichier/répertoire
        if (stat(full_path, &statbuf) == -1)
            continue;
        
        // Ajout de l'indentation en fonction du niveau
        for (int i = 0; i < level; i++) {
            size_t safe_space = output_size - *current_size - 1;
            const char *indent = (i == level - 1) ? "├── " : "│   ";
            size_t indent_len = strlen(indent);
            
            if (safe_space > indent_len) {
                memcpy(output + *current_size, indent, indent_len);
                *current_size += indent_len;
            } else {
                break; // Plus d'espace disponible
            }
        }
        
        // Ajout du nom de l'entrée avec vérification des limites
        size_t name_len = strlen(entry->d_name);
        size_t safe_space = output_size - *current_size - 10; // Garde un peu d'espace pour la suite
        
        if (name_len <= safe_space) {
            // Assez d'espace pour le nom complet
            memcpy(output + *current_size, entry->d_name, name_len);
            *current_size += name_len;
        } else if (safe_space > 5) {
            // Pas assez d'espace, tronquer le nom
            memcpy(output + *current_size, entry->d_name, safe_space - 3);
            memcpy(output + *current_size + safe_space - 3, "...", 3);
            *current_size += safe_space;
        }
        
        // Ajout d'un indicateur pour les répertoires ou retour à la ligne pour les fichiers
        if (S_ISDIR(statbuf.st_mode)) {
            if (output_size - *current_size > 2) {
                memcpy(output + *current_size, "/\n", 2);
                *current_size += 2;
                output[*current_size] = '\0';
                
                // Explorer récursivement les sous-répertoires (limiter la profondeur à 5 niveaux)
                if (level < 5) {
                    build_directory_tree(full_path, output, output_size, level + 1, current_size);
                } else if (level == 5 && output_size - *current_size > 40) {
                    // Indiquer qu'il y a plus de contenu mais trop profond
                    for (int i = 0; i <= level && output_size - *current_size > 5; i++) {
                        if (output_size - *current_size > 4) {
                            memcpy(output + *current_size, "    ", 4);
                            *current_size += 4;
                        }
                    }
                    
                    if (output_size - *current_size > 30) {
                        const char *depth_msg = "... (profondeur maximale atteinte)\n";
                        size_t msg_len = strlen(depth_msg);
                        if (msg_len < output_size - *current_size - 1) {
                            memcpy(output + *current_size, depth_msg, msg_len);
                            *current_size += msg_len;
                        }
                    }
                }
            }
        } else {
            if (output_size - *current_size > 1) {
                output[*current_size] = '\n';
                *current_size += 1;
                output[*current_size] = '\0';
            }
        }
    }
    
    closedir(dir);
}

// Fonction sécurisée pour explorer un répertoire et générer sa structure
static char* explore_directory(const char *path) {
    struct stat path_stat;
    size_t output_size = 10240; // Taille initiale de 10KB
    size_t current_size = 0;
    char *output = malloc(output_size);
    
    if (!output) {
        return NULL; // Échec de l'allocation
    }
    
    // Vérifier si le chemin existe
    if (stat(path, &path_stat) == -1) {
        snprintf(output, output_size, "Erreur: Le chemin '%s' n'existe pas ou n'est pas accessible\n", path);
        return output;
    }
    
    // Vérifier si c'est un répertoire
    if (!S_ISDIR(path_stat.st_mode)) {
        snprintf(output, output_size, "Erreur: '%s' n'est pas un répertoire\n", path);
        return output;
    }
    
    // Ajouter l'en-tête avec vérification de la taille
    current_size = snprintf(output, output_size, "Structure du répertoire: %s\n\n", path);
    if (current_size >= output_size) {
        free(output);
        return strdup("Erreur: Chemin trop long");
    }
    
    // Construire l'arborescence du répertoire de manière récursive
    build_directory_tree(path, output, output_size, 0, &current_size);
    
    return output;
}

// Fonction pour lister le contenu d'un répertoire en format JSON
int list_directory(const char *path, char *response) {
    DIR *dir;
    struct dirent *entry;
    struct stat statbuf;
    char full_path[MAX_PATH_LEN];
    
    // Tableau pour stocker les noms des fichiers et dossiers
    char **dir_entries = NULL;
    int entry_count = 0;
    int max_entries = 100; // Limitation du nombre d'entrées pour éviter un débordement
    
    // S'assurer que le buffer response commence avec une chaîne vide
    response[0] = '\0';
    
    // Allouer de la mémoire pour le tableau de noms
    dir_entries = malloc(max_entries * sizeof(char *));
    if (!dir_entries) {
        strncpy(response, "{\"error\": \"Erreur d'allocation mémoire\"}", BUFFER_SIZE - 1);
        response[BUFFER_SIZE - 1] = '\0';  // Garantir la terminaison
        return -1;
    }
    
    // Ouvrir le répertoire
    dir = opendir(path);
    if (!dir) {
        snprintf(response, BUFFER_SIZE - 1, "{\"error\": \"Impossible d'ouvrir le répertoire %s\"}", path);
        response[BUFFER_SIZE - 1] = '\0';  // Garantir la terminaison
        free(dir_entries);
        return -1;
    }
    
    // Lire le contenu du répertoire
    while ((entry = readdir(dir)) != NULL && entry_count < max_entries) {
        // Ignorer . et .. sauf si c'est le répertoire racine
        if (strcmp(path, "/") != 0 && (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0))
            continue;
            
        // Construire le chemin complet
        if (snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name) >= sizeof(full_path)) {
            // Chemin trop long, ignorer cette entrée
            continue;
        }
        
        // Obtenir les informations sur le fichier/dossier
        if (stat(full_path, &statbuf) == -1)
            continue;
            
        // Allouer de la mémoire pour le nom (+ éventuellement "/" pour les dossiers)
        size_t name_len = strlen(entry->d_name);
        dir_entries[entry_count] = malloc(name_len + 2);  // +2 pour le '/' potentiel et le '\0'
        if (!dir_entries[entry_count]) {
            continue; // Ignorer cette entrée en cas d'échec d'allocation
        }
        
        // Copier le nom et ajouter "/" pour les dossiers
        strncpy(dir_entries[entry_count], entry->d_name, name_len + 1);
        if (S_ISDIR(statbuf.st_mode)) {
            strcat(dir_entries[entry_count], "/");
        }
        
        entry_count++;
    }
    
    closedir(dir);
    
    // Générer la réponse JSON
    int pos = 0;
    int remaining = BUFFER_SIZE - 1;  // -1 pour garantir toujours de l'espace pour le '\0'
    
    // Début du JSON - vérifier qu'il y a assez d'espace
    int written = snprintf(response + pos, remaining, "{\"path\": \"%s\", \"contents\": [", path);
    if (written >= remaining) {
        // Le buffer est trop petit même pour l'en-tête
        strncpy(response, "{\"error\": \"Buffer trop petit\"}", BUFFER_SIZE - 1);
        response[BUFFER_SIZE - 1] = '\0';
        
        // Libérer la mémoire
        for (int i = 0; i < entry_count; i++) {
            free(dir_entries[i]);
        }
        free(dir_entries);
        return -1;
    }
    
    pos += written;
    remaining -= written;
    
    // Ajouter chaque entrée, en vérifiant qu'il reste toujours de l'espace
    for (int i = 0; i < entry_count && remaining > 2; i++) {  // minimum 2 pour ", " ou "]}"
        // Ajouter une virgule sauf pour le premier élément
        if (i > 0) {
            if (remaining < 2) break;  // Pas assez d'espace
            strncpy(response + pos, ", ", 2);
            pos += 2;
            remaining -= 2;
        }
        
        // Allouer un buffer suffisant pour le nom échappé
        size_t name_len = strlen(dir_entries[i]);
        // Dans le pire cas, chaque caractère pourrait nécessiter un échappement (\u + 4 chiffres hex)
        char *escaped_name = malloc(name_len * 6 + 1);
        if (!escaped_name) continue;  // Ignorer cette entrée
        
        int escaped_pos = 0;
        
        // Échapper les caractères spéciaux
        for (size_t j = 0; j < name_len; j++) {
            char c = dir_entries[i][j];
            
            if (c == '"' || c == '\\' || c == '\b' || c == '\f' || c == '\n' || c == '\r' || c == '\t') {
                escaped_name[escaped_pos++] = '\\';
                
                switch (c) {
                    case '"': escaped_name[escaped_pos++] = '"'; break;
                    case '\\': escaped_name[escaped_pos++] = '\\'; break;
                    case '\b': escaped_name[escaped_pos++] = 'b'; break;
                    case '\f': escaped_name[escaped_pos++] = 'f'; break;
                    case '\n': escaped_name[escaped_pos++] = 'n'; break;
                    case '\r': escaped_name[escaped_pos++] = 'r'; break;
                    case '\t': escaped_name[escaped_pos++] = 't'; break;
                }
            } else {
                escaped_name[escaped_pos++] = c;
            }
        }
        
        escaped_name[escaped_pos] = '\0';
        
        // Calculer l'espace nécessaire pour cette entrée (guillemets inclus)
        int needed_space = escaped_pos + 2;  // +2 pour les guillemets
        
        if (needed_space > remaining) {
            // Pas assez d'espace pour cette entrée
            free(escaped_name);
            break;
        }
        
        // Ajouter le nom échappé à la réponse JSON
        response[pos++] = '"';
        remaining--;
        
        strncpy(response + pos, escaped_name, remaining);
        size_t copy_len = (escaped_pos < remaining) ? escaped_pos : remaining;
        pos += copy_len;
        remaining -= copy_len;
        
        if (remaining > 0) {
            response[pos++] = '"';
            remaining--;
        }
        
        free(escaped_name);
    }
    
    // Fin du JSON
    if (remaining >= 2) {
        strncpy(response + pos, "]}", 2);
        pos += 2;
    } else if (remaining == 1) {
        response[pos++] = ']';
    }
    
    // Assurer que la chaîne est bien terminée
    response[pos < BUFFER_SIZE ? pos : BUFFER_SIZE - 1] = '\0';
    
    // Libérer la mémoire allouée
    for (int i = 0; i < entry_count; i++) {
        free(dir_entries[i]);
    }
    free(dir_entries);
    
    return 0;
}

// Function to stop the web server
int stop_web_interface(void) {
    // Read the PID from the file
    pid_t pid = read_pid_from_file();
    if (pid <= 0) {
        printf("Web server is not running or PID file not found.\n");
        return EXIT_FAILURE;
    }
    
    // Send SIGTERM to the process
    if (kill(pid, SIGTERM) == -1) {
        // If process doesn't exist, remove PID file and report error
        if (errno == ESRCH) {
            printf("Web server process doesn't exist. Cleaning up PID file...\n");
            unlink(PID_FILE);
            return EXIT_FAILURE;
        }
        perror("Failed to send termination signal to web server");
        return EXIT_FAILURE;
    }
    
    // Wait a moment for the process to terminate
    usleep(100000); // 100ms
    
    // Check if the process still exists
    if (kill(pid, 0) == -1 && errno == ESRCH) {
        printf("Web server stopped successfully.\n");
        // Remove PID file after successful termination
        unlink(PID_FILE);
        return EXIT_SUCCESS;
    } else {
        printf("Web server is still running. You may need to use 'pkill -f mkdf' to force termination.\n");
        return EXIT_FAILURE;
    }
}

// Function signature corrected to match declaration in header
int start_web_interface(void) {
    // Check if server is already running
    pid_t existing_pid = read_pid_from_file();
    if (existing_pid > 0) {
        // Check if the process with this PID exists
        if (kill(existing_pid, 0) == 0) {
            printf("Web server is already running at http://localhost:%d (PID: %d)\n", PORT, existing_pid);
            printf("To stop the server, use: mkdf --stop\n");
            return EXIT_FAILURE;
        } else {
            // Process doesn't exist, clean up stale PID file
            printf("Cleaning up stale PID file...\n");
            unlink(PID_FILE);
        }
    }

    // Set up signal handlers for graceful termination
    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);
    
    // Save PID to file
    if (save_pid_to_file(getpid()) != 0) {
        perror("Failed to save PID file");
        return EXIT_FAILURE;
    }

    // Create socket
    int server_fd;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    
    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        return EXIT_FAILURE;
    }
    
    // Allow socket reuse
    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt");
        close(server_fd);
        return EXIT_FAILURE;
    }
    
    // Set up server address structure
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    
    // Bind the socket to the port
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        close(server_fd);
        return EXIT_FAILURE;
    }
    
    // Listen for connections
    if (listen(server_fd, 10) < 0) {
        perror("listen");
        close(server_fd);
        return EXIT_FAILURE;
    }

    printf("Web server started on http://localhost:%d\n", PORT);
    printf("Press Ctrl+C to stop the server\n");
    
    // Accept and handle incoming connections
    while (1) {
        int new_socket;
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0) {
            perror("accept");
            continue;
        }
        
        // Create a thread to handle the client
        thread_args_t *args = malloc(sizeof(thread_args_t));
        if (!args) {
            perror("malloc failed");
            close(new_socket);
            continue;
        }
        
        args->client_fd = new_socket;
        
        pthread_t thread_id;
        if (pthread_create(&thread_id, NULL, handle_client, args) != 0) {
            perror("pthread_create failed");
            free(args);
            close(new_socket);
        }
        
        // Detach the thread so it cleans up automatically
        pthread_detach(thread_id);
    }

    // Cleanup (this won't be reached unless there's an error)
    close(server_fd);
    unlink(PID_FILE);
    return EXIT_SUCCESS;
}

// Function to start web interface with custom port
int start_web_interface_with_port(int port) {
    // Check if server is already running
    pid_t existing_pid = read_pid_from_file();
    if (existing_pid > 0) {
        // Check if the process with this PID exists
        if (kill(existing_pid, 0) == 0) {
            printf("Web server is already running (PID: %d)\n", existing_pid);
            printf("To stop the server, use: mkdf --stop\n");
            return EXIT_FAILURE;
        } else {
            // Process doesn't exist, clean up stale PID file
            printf("Cleaning up stale PID file...\n");
            unlink(PID_FILE);
        }
    }

    // Set up signal handlers for graceful termination
    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);
    
    // Save PID to file
    if (save_pid_to_file(getpid()) != 0) {
        perror("Failed to save PID file");
        return EXIT_FAILURE;
    }

    // Create socket
    int server_fd;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    
    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        return EXIT_FAILURE;
    }
    
    // Allow socket reuse
    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt");
        close(server_fd);
        return EXIT_FAILURE;
    }
    
    // Set up server address structure
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);
    
    // Bind the socket to the port
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        close(server_fd);
        return EXIT_FAILURE;
    }
    
    // Listen for connections
    if (listen(server_fd, 10) < 0) {
        perror("listen");
        close(server_fd);
        return EXIT_FAILURE;
    }

    printf("Web server started on http://localhost:%d\n", port);
    printf("Press Ctrl+C to stop the server\n");
    
    // Accept and handle incoming connections
    while (1) {
        int new_socket;
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0) {
            perror("accept");
            continue;
        }
        
        // Create a thread to handle the client
        thread_args_t *args = malloc(sizeof(thread_args_t));
        if (!args) {
            perror("malloc failed");
            close(new_socket);
            continue;
        }
        
        args->client_fd = new_socket;
        
        pthread_t thread_id;
        if (pthread_create(&thread_id, NULL, handle_client, args) != 0) {
            perror("pthread_create failed");
            free(args);
            close(new_socket);
        }
        
        // Detach the thread so it cleans up automatically
        pthread_detach(thread_id);
    }

    // Cleanup (this won't be reached unless there's an error)
    close(server_fd);
    unlink(PID_FILE);
    return EXIT_SUCCESS;
}