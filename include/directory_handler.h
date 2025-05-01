#ifndef DIRECTORY_HANDLER_H
#define DIRECTORY_HANDLER_H

#include <stdlib.h>

// Codes de retour
#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1

// Types de projets supportés
typedef enum {
    PROJECT_SIMPLE,   // Structure de projet simple
    PROJECT_MULTI,    // Structure multi-répertoires
    PROJECT_DOCKER,   // Projet avec Docker
    PROJECT_FASTAPI,  // Projet FastAPI
    PROJECT_VUEVITE,  // Projet Vue+Vite
    PROJECT_REACT,    // Projet React
    PROJECT_FLASK,    // Projet Flask
    PROJECT_NODEJS,   // Projet Node.js
    PROJECT_NEXTJS,   // Projet Next.js
    PROJECT_NUXTJS,   // Projet Nuxt.js
} project_template_t;

/**
 * Active ou désactive la restriction des opérations au répertoire home
 * 
 * @param mode 1 pour activer, 0 pour désactiver
 */
void set_home_directory_restriction(int mode);

/**
 * Vérifie si la restriction au répertoire home est activée
 * 
 * @return 1 si activée, 0 sinon
 */
int is_home_directory_restriction(void);

/**
 * Vérifie si un chemin est dans le répertoire home de l'utilisateur
 * 
 * @param path Le chemin à vérifier
 * @return 1 si le chemin est dans le home, 0 sinon
 */
int is_path_in_home_directory(const char *path);

/**
 * Active la restriction au répertoire personnel
 */
void enable_home_directory_restriction(void);

/**
 * Désactive la restriction au répertoire personnel
 */
void disable_home_directory_restriction(void);

/**
 * Crée une structure de répertoires et de fichiers à partir d'un motif
 * contenant éventuellement des expressions d'accolades.
 * 
 * @param expression Le motif à utiliser pour créer la structure
 * @return EXIT_SUCCESS en cas de succès, EXIT_FAILURE sinon
 */
int create_directory_structure(const char *expression);

/**
 * Crée un répertoire de manière récursive
 * (équivalent à mkdir -p)
 * 
 * @param path Le chemin du répertoire à créer
 * @return 0 en cas de succès, -1 sinon
 */
int create_directory_recursive(const char *path);

/**
 * Remplace le tilde (~) par le chemin du répertoire personnel
 * 
 * @param path Le chemin avec un tilde
 * @param expanded_path Le buffer où stocker le chemin expansé
 * @param size La taille du buffer
 * @return 0 en cas de succès, -1 sinon
 */
int expand_tilde(const char *path, char *expanded_path, size_t size);

/**
 * Crée un projet à partir d'un template
 * 
 * @param path Le chemin où créer le projet
 * @return EXIT_SUCCESS en cas de succès, EXIT_FAILURE sinon
 */
int create_template_project(const char *path);

/**
 * Set the force mode (overwrite existing files/directories)
 * 
 * @param mode 1 to enable force mode, 0 to disable
 */
void set_force_mode(int mode);

/**
 * Set the verbose mode (display detailed output)
 * 
 * @param mode 1 to enable verbose mode, 0 to disable
 */
void set_verbose_mode(int mode);

/**
 * Set the quiet mode (suppress all output)
 * 
 * @param mode 1 to enable quiet mode, 0 to disable
 */
void set_quiet_mode(int mode);

/**
 * Check if force mode is enabled
 */
int is_force_mode(void);

/**
 * Check if verbose mode is enabled
 */
int is_verbose_mode(void);

/**
 * Check if quiet mode is enabled
 */
int is_quiet_mode(void);

/**
 * Crée un fichier à partir d'un template
 * 
 * @param dest_path Chemin où créer le fichier
 * @param template_path Chemin du fichier template à utiliser
 * @return 0 en cas de succès, -1 sinon
 */
int create_file_from_template(const char *dest_path, const char *template_path);

/**
 * Vérifie si une chaîne contient un template de fichier (format: file.txt:template.txt)
 * 
 * @param path La chaîne à vérifier
 * @return 1 si c'est un template, 0 sinon
 */
int is_template_path(const char *path);

/**
 * Extrait le nom du fichier destination et le chemin du template
 * 
 * @param path La chaîne au format "destination:template"
 * @param dest_path Buffer pour stocker le chemin de destination
 * @param template_path Buffer pour stocker le chemin du template
 * @param size Taille des buffers
 * @return 0 en cas de succès, -1 sinon
 */
int extract_template_info(const char *path, char *dest_path, char *template_path, size_t size);

#endif /* DIRECTORY_HANDLER_H */