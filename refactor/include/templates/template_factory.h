#ifndef TEMPLATE_FACTORY_H
#define TEMPLATE_FACTORY_H

#include <stdbool.h>
#include "template_types.h"

/**
 * Crée un projet en utilisant le template spécifié
 * 
 * @param type Type de template à utiliser
 * @param project_path Chemin où créer le projet
 * @param force Écraser si existe déjà
 * @return 0 si succès, -1 si erreur
 */
int create_template(TemplateType type, const char *project_path, bool force);

/**
 * Crée un projet en utilisant le nom du template
 * 
 * @param template_name Nom du template (ex: "simple", "low_level", etc.)
 * @param project_path Chemin où créer le projet
 * @param force Écraser si existe déjà
 * @return 0 si succès, -1 si erreur
 */
int create_template_by_name(const char *template_name, const char *project_path, bool force);

/**
 * Convertit un nom de template en type énuméré
 * 
 * @param template_name Nom du template
 * @return Type de template correspondant, ou -1 si non trouvé
 */
TemplateType get_template_type_by_name(const char *template_name);

#endif /* TEMPLATE_FACTORY_H */
