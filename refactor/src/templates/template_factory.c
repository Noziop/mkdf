#include "../include/templates/template_factory.h"
#include "../include/templates/template_manager.h"
#include "../include/templates/base/base_templates.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * Crée un projet en utilisant le template spécifié
 */
int create_template(TemplateType type, const char *project_path, bool force) {
    if (!project_path) return -1;
    
    switch (type) {
        case TEMPLATE_SIMPLE:
            return create_simple_project(project_path, force);
        
        case TEMPLATE_LOW_LEVEL:
            return create_low_level_project(project_path, force);
        
        // Les autres types de templates seront implémentés progressivement
        // case TEMPLATE_REACT:
        //     return create_react_project(project_path, force);
        // etc.
        
        default:
            fprintf(stderr, "Type de template non implémenté: %d\n", type);
            return -1;
    }
}

/**
 * Crée un projet en utilisant le nom du template
 */
int create_template_by_name(const char *template_name, const char *project_path, bool force) {
    if (!template_name || !project_path) return -1;
    
    TemplateType type = get_template_type_by_name(template_name);
    if ((int)type == -1) {
        fprintf(stderr, "Template inconnu: %s\n", template_name);
        fprintf(stderr, "Templates disponibles: simple, low_level, react, vue, flask, fastapi, ...\n");
        return -1;
    }
    
    return create_template(type, project_path, force);
}

/**
 * Convertit un nom de template en type énuméré
 */
TemplateType get_template_type_by_name(const char *template_name) {
    if (!template_name) return (TemplateType)-1;
    
    // Récupérer tous les templates disponibles
    int count;
    const Template **all_templates = get_all_templates(&count);
    if (!all_templates) return (TemplateType)-1;
    
    // Chercher un template correspondant au nom
    TemplateType result = (TemplateType)-1;
    for (int i = 0; i < count; i++) {
        if (strcmp(all_templates[i]->name, template_name) == 0) {
            result = all_templates[i]->type;
            break;
        }
    }
    
    free(all_templates);
    return result;
}
