#include "../include/fs/dir_creator.h"
#include "../include/fs/path_analyzer.h"
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/**
 * Crée un répertoire simple (équivalent à mkdir)
 */
int create_directory(const char *path) {
    if (!path) return -1;
    
    // Vérifier si le répertoire existe déjà
    if (directory_exists(path)) {
        return 0;  // Considérer comme un succès si le répertoire existe déjà
    }
    
    // Créer le répertoire avec les permissions 0755 (rwxr-xr-x)
    if (mkdir(path, 0755) != 0) {
        fprintf(stderr, "Erreur lors de la création du répertoire '%s': %s\n", 
                path, strerror(errno));
        return -1;
    }
    
    // Mode verbeux : afficher un message de succès
    printf("Created directory: %s\n", path);
    return 0;
}

/**
 * Vérifie si un répertoire existe
 */
bool directory_exists(const char *path) {
    if (!path) return false;
    
    struct stat st;
    if (stat(path, &st) == 0) {
        return S_ISDIR(st.st_mode);
    }
    return false;
}

/**
 * Crée un répertoire et tous ses parents si nécessaire (mkdir -p)
 */
int create_directory_recursive(const char *path, bool force) {
    if (!path) return -1;

    // Ajout du paramètre force    
    if (directory_exists(path)) {
        if (!force) {
            printf("Le répertoire '%s' existe déjà. Continuer ? (y/n) ", path);
            char response = getchar();
            if (response != 'y' && response != 'Y') return 0;
        }
        return 0;
    }
    
    // Si le répertoire existe déjà, rien à faire
    if (directory_exists(path)) {
        return 0;
    }
    
    // Copier le chemin pour pouvoir le modifier
    char *temp_path = strdup(path);
    if (!temp_path) {
        fprintf(stderr, "Erreur d'allocation mémoire\n");
        return -1;
    }
    
    // Normaliser le chemin en remplaçant les séparateurs multiples
    char *p = temp_path;
    char *q = temp_path;
    bool was_slash = false;
    
    while (*p) {
        if (*p == '/') {
            if (!was_slash) {
                *q++ = *p;
            }
            was_slash = true;
        } else {
            *q++ = *p;
            was_slash = false;
        }
        p++;
    }
    *q = '\0';  // Terminer la chaîne
    
    // Créer chaque niveau du chemin
    for (p = temp_path + 1; *p; p++) {
        if (*p == '/') {
            *p = '\0';  // Couper temporairement la chaîne
            
            if (strlen(temp_path) > 0 && !directory_exists(temp_path)) {
                if (mkdir(temp_path, 0755) != 0 && errno != EEXIST) {
                    fprintf(stderr, "Erreur lors de la création du répertoire '%s': %s\n", 
                            temp_path, strerror(errno));
                    free(temp_path);
                    return -1;
                }
            }
            
            *p = '/';  // Restaurer le séparateur
        }
    }
    
    // Créer le répertoire final
    int result = create_directory(temp_path);
    
    free(temp_path);
    return result;
}

/**
 * Crée une structure de répertoires d'après un chemin
 */
int create_directory_structure(const char *path, bool force) {
    if (!path) return -1;
    
    // Vérifier que le chemin est bien un répertoire
    if (!is_directory_path(path)) {
        fprintf(stderr, "Le chemin '%s' ne semble pas être un répertoire\n", path);
        return -1;
    }
    
    // Vérifier si le répertoire existe déjà
    if (directory_exists(path)) {
        if (!force) {
            fprintf(stderr, "Le répertoire '%s' existe déjà. Utilisez l'option --force pour écraser.\n", path);
            return -1;
        }
    }
    
    // Créer le répertoire et ses parents
    return create_directory_recursive(path, force);
}
