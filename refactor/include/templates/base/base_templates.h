#ifndef BASE_TEMPLATES_H
#define BASE_TEMPLATES_H

#include <stdbool.h>
#include "../template_types.h"

/**
 * Crée un projet avec le template "simple"
 * 
 * @param project_path Chemin où créer le projet
 * @param force Écraser si existe déjà
 * @return 0 si succès, -1 si erreur
 */
int create_simple_project(const char *project_path, bool force);

/**
 * Crée un projet avec le template "low_level" (ancien "multi")
 * 
 * @param project_path Chemin où créer le projet
 * @param force Écraser si existe déjà
 * @return 0 si succès, -1 si erreur
 */
int create_low_level_project(const char *project_path, bool force);

/**
 * Obtient les chemins pour le template "simple"
 * 
 * @return Tableau de chemins relatifs à créer
 */
const char** get_simple_template_paths(int *count);

/**
 * Obtient les chemins pour le template "low_level"
 * 
 * @return Tableau de chemins relatifs à créer
 */
const char** get_low_level_template_paths(int *count);

#endif /* BASE_TEMPLATES_H */
