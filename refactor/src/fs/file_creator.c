#include "../include/fs/file_creator.h"
#include "../include/fs/path_analyzer.h"
#include "../include/fs/dir_creator.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <libgen.h>

/**
 * Vérifie si un fichier existe
 */
bool file_exists(const char *path) {
    if (!path) return false;
    
    struct stat st;
    if (stat(path, &st) == 0) {
        return S_ISREG(st.st_mode);
    }
    return false;
}

/**
 * Crée un fichier vide à l'emplacement spécifié
 */
int create_empty_file(const char *path, bool force) {
    if (!path) return -1;

    // Vérifier si le fichier existe déjà et ajout du paramètre force
    if (file_exists(path)) {
        if (!force) {
            printf("Le fichier '%s' existe déjà. Écraser ? (y/n) ", path);
            char response = getchar();
            if (response != 'y' && response != 'Y') return 0;
        }
    }
    
    // Ouvrir le fichier en écriture, le créer s'il n'existe pas
    FILE *file = fopen(path, "w");
    if (!file) {
        fprintf(stderr, "Erreur lors de la création du fichier '%s': %s\n", 
                path, strerror(errno));
        return -1;
    }
    
    fclose(file);
    printf("Created file: %s\n", path);
    return 0;
}

/**
 * Crée un fichier à partir d'un template
 */
int create_file_from_template(const char *path, const char *template_path) {
    if (!path || !template_path) return -1;
    
    // Vérifier si le template existe
    if (!file_exists(template_path)) {
        fprintf(stderr, "Le fichier template '%s' n'existe pas\n", template_path);
        return -1;
    }
    
    // Ouvrir le fichier template en lecture
    FILE *template_file = fopen(template_path, "r");
    if (!template_file) {
        fprintf(stderr, "Erreur lors de l'ouverture du template '%s': %s\n", 
                template_path, strerror(errno));
        return -1;
    }
    
    // Ouvrir le fichier de destination en écriture
    FILE *dest_file = fopen(path, "w");
    if (!dest_file) {
        fprintf(stderr, "Erreur lors de la création du fichier '%s': %s\n", 
                path, strerror(errno));
        fclose(template_file);
        return -1;
    }
    
    // Copier le contenu du template vers le fichier de destination
    char buffer[4096];
    size_t bytes;
    
    while ((bytes = fread(buffer, 1, sizeof(buffer), template_file)) > 0) {
        fwrite(buffer, 1, bytes, dest_file);
    }
    
    fclose(template_file);
    fclose(dest_file);
    
    printf("Created file from template: %s (using %s)\n", path, template_path);
    return 0;
}

/**
 * Fonction principale pour créer un fichier
 */
int create_file(const char *path, bool force) {
    if (!path) return -1;
    
    // Vérifier si le chemin correspond à un fichier
    if (!is_file_path(path)) {
        fprintf(stderr, "Le chemin '%s' ne semble pas être un fichier\n", path);
        return -1;
    }
    
    // Vérifier si le fichier existe déjà
    if (file_exists(path) && !force) {
        fprintf(stderr, "Le fichier '%s' existe déjà. Utilisez l'option --force pour écraser.\n", path);
        return -1;
    }
    
    // Créer le répertoire parent si nécessaire
    char *path_copy = strdup(path);
    if (!path_copy) {
        fprintf(stderr, "Erreur d'allocation mémoire\n");
        return -1;
    }
    
    char *parent_dir = dirname(path_copy);
    if (strlen(parent_dir) > 0 && strcmp(parent_dir, ".") != 0) {
        create_directory_recursive(parent_dir, force);
    }
    
    free(path_copy);
    
    // Vérifier si le chemin utilise un template
    if (is_template_path(path)) {
        char dest_path[4096];
        char template_path[4096];
        
        if (extract_template_info(path, dest_path, template_path, sizeof(dest_path)) != 0) {
            fprintf(stderr, "Erreur lors de l'extraction des informations de template\n");
            return -1;
        }
        
        // Créer le fichier à partir du template
        return create_file_from_template(dest_path, template_path);
    } else {
        // Créer un fichier vide
        return create_empty_file(path, force);
    }
}
