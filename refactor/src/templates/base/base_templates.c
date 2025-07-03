#include "../../../include/templates/base/base_templates.h"
#include "../../../include/fs/dir_creator.h"
#include "../../../include/fs/file_creator.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Définition des chemins pour le template "simple"
static const char *simple_template_paths[] = {
    "src/",
    "docs/",
    "tests/",
    "README.md"
};

// Définition des chemins pour le template "low_level" (ancien "multi")
static const char *low_level_template_paths[] = {
    "src/lib/",
    "src/bin/",
    "src/include/",
    "docs/user/",
    "docs/dev/",
    "tests/",
    "examples/",
    "README.md",
    "LICENSE"
};

/**
 * Obtient les chemins pour le template "simple"
 */
const char** get_simple_template_paths(int *count) {
    *count = sizeof(simple_template_paths) / sizeof(simple_template_paths[0]);
    return simple_template_paths;
}

/**
 * Obtient les chemins pour le template "low_level"
 */
const char** get_low_level_template_paths(int *count) {
    *count = sizeof(low_level_template_paths) / sizeof(low_level_template_paths[0]);
    return low_level_template_paths;
}

/**
 * Fonction utilitaire pour créer un projet à partir d'un tableau de chemins
 */
static int create_project_from_paths(const char *project_path, const char **paths, int path_count, bool force) {
    if (!project_path || !paths) return -1;
    
    char full_path[4096];
    
    // Créer le répertoire principal du projet
    if (create_directory_recursive(project_path) != 0) {
        fprintf(stderr, "Erreur lors de la création du répertoire principal '%s'\n", project_path);
        return -1;
    }
    
    // Créer chaque élément du template
    for (int i = 0; i < path_count; i++) {
        snprintf(full_path, sizeof(full_path), "%s/%s", project_path, paths[i]);
        
        // Déterminer s'il s'agit d'un fichier ou d'un répertoire
        if (paths[i][strlen(paths[i]) - 1] == '/') {
            // C'est un répertoire
            if (create_directory_recursive(full_path) != 0) {
                fprintf(stderr, "Erreur lors de la création du répertoire '%s'\n", full_path);
                return -1;
            }
        } else {
            // C'est un fichier
            if (create_empty_file(full_path) != 0) {
                fprintf(stderr, "Erreur lors de la création du fichier '%s'\n", full_path);
                return -1;
            }
        }
    }
    
    printf("Projet créé avec succès à '%s'\n", project_path);
    return 0;
}

/**
 * Crée un projet avec le template "simple"
 */
int create_simple_project(const char *project_path, bool force) {
    int count;
    const char **paths = get_simple_template_paths(&count);
    return create_project_from_paths(project_path, paths, count, force);
}

/**
 * Crée un projet avec le template "low_level"
 */
int create_low_level_project(const char *project_path, bool force) {
    int count;
    const char **paths = get_low_level_template_paths(&count);
    return create_project_from_paths(project_path, paths, count, force);
}
