#ifndef TEMPLATE_TYPES_H
#define TEMPLATE_TYPES_H

/**
 * Énumération des types de templates disponibles
 */
typedef enum {
    TEMPLATE_SIMPLE,        // Structure simple
    TEMPLATE_LOW_LEVEL,     // Structure pour projet en C/C++ (ancien "multi")
    TEMPLATE_REACT,         // Application React
    TEMPLATE_VUE,           // Application Vue.js + Vite
    TEMPLATE_FLASK,         // Application Flask (Python)
    TEMPLATE_FASTAPI,       // API FastAPI (Python)
    TEMPLATE_EXPRESS,       // Application Express.js (Node)
    TEMPLATE_SLIM,          // Application Slim (PHP)
    TEMPLATE_LARAVEL,       // Application Laravel (PHP)
    TEMPLATE_DOCKER_BASE,   // Configuration Docker basique
    TEMPLATE_DOCKER_FULL,   // Ensemble Docker complet
    // Ajouter ici les futurs templates
} TemplateType;

#endif /* TEMPLATE_TYPES_H */
