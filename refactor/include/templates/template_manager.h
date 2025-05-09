#ifndef TEMPLATE_MANAGER_H
#define TEMPLATE_MANAGER_H

#include <stdbool.h>
#include "template_types.h"

/**
 * Structure pour stocker les informations d'un template
 */
typedef struct {
    char *name;             // Nom du template
    char *description;      // Description du template
    char **paths;           // Tableau de chemins à créer
    int path_count;         // Nombre de chemins
    TemplateType type;      // Type de template
} Template;

/**
 * Crée un projet à partir d'un template
 * 
 * @param type Type de template à utiliser
 * @param project_path Chemin où créer le projet
 * @param force Écraser si existe déjà
 * @return 0 si succès, -1 si erreur
 */
int create_project_from_template(TemplateType type, const char *project_path, bool force);

/**
 * Récupère les informations d'un template
 * 
 * @param type Type de template
 * @return Pointeur vers la structure Template correspondante
 */
const Template* get_template_info(TemplateType type);

/**
 * Récupère la liste de tous les templates disponibles
 * 
 * @param count Pointeur pour stocker le nombre de templates
 * @return Tableau de pointeurs vers les templates
 */
const Template** get_all_templates(int *count);

#endif /* TEMPLATE_MANAGER_H */
