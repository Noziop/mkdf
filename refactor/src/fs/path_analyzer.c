#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <pwd.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <limits.h>
#include "../include/fs/path_analyzer.h"

/**
 * Détermine si un chemin correspond à un répertoire, basé sur plusieurs heuristiques
 */
bool is_directory_path(const char *path) {
    // Vérifier si le chemin est nul ou vide
    if (!path) {
        fprintf(stderr, "Erreur : chemin NULL passé à is_directory_path()\n");
        return false;
    }
    
    size_t len = strlen(path);
    
    // Règle 1: Si le chemin se termine par '/', c'est un répertoire
    if (len > 0 && path[len - 1] == '/') {
        return true;
    }
    
    // Règle 2: Si le chemin existe et est un répertoire, retourner vrai
    struct stat st;
    if (stat(path, &st) == 0) {
        return S_ISDIR(st.st_mode);
    }
    
    // Règle 3: Si le chemin n'a pas d'extension, c'est probablement un répertoire
    // (à moins qu'il ne se termine par un point, ce qui est rare pour un répertoire)
    const char *last_dot = strrchr(path, '.');
    const char *last_slash = strrchr(path, '/');
    
    // Si pas de point ou si le dernier point est avant le dernier slash,
    // c'est probablement un répertoire
    if (!last_dot || (last_slash && last_dot < last_slash)) {
        return true;
    }
    
    // Par défaut, si aucune autre règle ne s'applique, considérer comme fichier
    return false;
}

/**
 * Détermine si un chemin correspond à un fichier
 */
bool is_file_path(const char *path) {
    if (!path) return false;
    
    // Un chemin est un fichier s'il n'est pas un répertoire
    return !is_directory_path(path);
}

/**
 * Vérifie si un chemin se trouve dans le home directory
 */
bool is_path_in_home_directory(const char *path) {
    if (!path || path[0] == '\0') {
        return false;
    }
    
    // Obtenir le répertoire home de l'utilisateur
    const char *home = getenv("HOME");
    if (home == NULL) {
        // Si HOME n'est pas défini, essayer de l'obtenir via getpwuid
        struct passwd *pw = getpwuid(getuid());
        if (pw == NULL) {
            return false;
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
                return true;
            }
        }
        return false;
    }
    
    // Si le chemin est relatif au home (~)
    else if (path[0] == '~' && (path[1] == '/' || path[1] == '\0')) {
        return true;
    }
    
    // Si le chemin est relatif, vérifier si le répertoire courant est dans le home
    else {
        char cwd[4096];
        if (getcwd(cwd, sizeof(cwd)) == NULL) {
            return false; // En cas d'erreur, considérer comme non sûr
        }
        
        // Vérifier si le répertoire courant est dans le home
        size_t home_len = strlen(home);
        if (strncmp(cwd, home, home_len) == 0) {
            // S'assurer qu'après le home, il y a soit un slash, soit rien
            if (cwd[home_len] == '/' || cwd[home_len] == '\0') {
                return true;
            }
        }
        return false;
    }
}

/**
 * Expande le tilde (~) dans un chemin
 */
int expand_tilde(const char *path, char *expanded_path, size_t size) {
    if (path == NULL || expanded_path == NULL) {
        return -1;
    }
    
    // Vérifie si le chemin commence par un tilde
    if (path[0] == '~' && (path[1] == '/' || path[1] == '\0')) {
        const char *home = getenv("HOME");
        if (home == NULL) {
            // Si HOME n'est pas défini, essayer de l'obtenir via getpwuid
            struct passwd *pw = getpwuid(getuid());
            if (pw == NULL) {
                return -1;
            }
            home = pw->pw_dir;
        }
        
        // Combiner le répertoire personnel avec le reste du chemin
        if (path[1] == '\0') {
            // Juste "~"
            snprintf(expanded_path, size, "%s", home);
        } else {
            // "~/quelque-chose"
            snprintf(expanded_path, size, "%s%s", home, path + 1);
        }
    } else {
        // Pas de tilde, simplement copier le chemin
        strncpy(expanded_path, path, size);
        expanded_path[size - 1] = '\0';
    }
    
    return 0;
}

/**
 * Vérifie si un chemin utilise un template
 */
bool is_template_path(const char *path) {
    if (!path) return false;
    
    // Vérifier si le chemin contient ":" mais pas au début
    // (pour éviter les chemins Windows comme C:\...)
    const char *colon = strchr(path, ':');
    if (colon && colon != path) {
        // Vérifier qu'il y a du contenu après les deux côtés du :
        if (colon[1] != '\0' && colon != path) {
            return true;
        }
    }
    
    return false;
}

/**
 * Extrait les infos d'un chemin template
 */
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
    dest_path[dest_len] = '\0';
    
    strncpy(template_path, colon + 1, size - 1);
    template_path[size - 1] = '\0';
    
    return 0;
}

/**
 * Vérifie si un chemin est valide 
 */
bool is_valid_path(const char *path) {
    if (!path) return false;
    if (strlen(path) > PATH_MAX) {
        fprintf(stderr, "Chemin trop long (max %d caractères)\n", PATH_MAX);
        return false;
    }
    return true;
}
