#include "../include/templates/template_manager.h"
#include "../include/templates/template_factory.h"
#include "../include/templates/base/base_templates.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Tableau des templates disponibles
static Template templates[] = {
    {
        .name = "simple",
        .description = "Structure de projet simple",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_SIMPLE
    },
    {
        .name = "low_level",
        .description = "Structure pour projet en C/C++ (ancien \"multi\")",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_LOW_LEVEL
    },
    {
        .name = "react",
        .description = "Application React",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_REACT
    },
    {
        .name = "vue",
        .description = "Application Vue.js + Vite",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_VUE
    },
    {
        .name = "flask",
        .description = "Application Flask (Python)",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_FLASK
    },
    {
        .name = "fastapi",
        .description = "API FastAPI (Python)",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_FASTAPI
    },
    {
        .name = "express",
        .description = "Application Express.js (Node)",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_EXPRESS
    },
    {
        .name = "slim",
        .description = "Application Slim PHP",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_SLIM
    },
    {
        .name = "laravel",
        .description = "Application Laravel PHP",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_LARAVEL
    },
    {
        .name = "docker_base",
        .description = "Configuration Docker de base",
        .paths = NULL,
        .path_count = 0,
        .type = TEMPLATE_DOCKER_BASE
    }
};

// Nombre de templates disponibles
static const int template_count = sizeof(templates) / sizeof(templates[0]);

/**
 * Crée un projet à partir d'un template
 */
int create_project_from_template(TemplateType type, const char *project_path, bool force) {
    // Déléguer à la factory
    return create_template(type, project_path, force);
}

/**
 * Récupère les informations d'un template
 */
const Template* get_template_info(TemplateType type) {
    for (int i = 0; i < template_count; i++) {
        if (templates[i].type == type) {
            return &templates[i];
        }
    }
    return NULL;
}

/**
 * Récupère la liste de tous les templates disponibles
 */
const Template** get_all_templates(int *count) {
    if (!count) return NULL;
    
    *count = template_count;
    
    // Allouer de la mémoire pour un tableau de pointeurs vers les templates
    const Template **result = malloc(template_count * sizeof(Template*));
    if (!result) return NULL;
    
    // Remplir le tableau avec des pointeurs vers chaque template
    for (int i = 0; i < template_count; i++) {
        result[i] = &templates[i];
    }
    
    return result;
}
