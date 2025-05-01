#ifndef CLI_HANDLER_H
#define CLI_HANDLER_H

#include "directory_handler.h"  // Inclusion du fichier directory_handler.h pour utiliser project_template_t

/**
 * Démarre le mode CLI interactif
 * 
 * @return EXIT_SUCCESS en cas de succès, EXIT_FAILURE en cas d'erreur
 */
int start_cli_mode(void);

/**
 * Affiche la structure de répertoires du chemin spécifié
 * 
 * @param path Le chemin à afficher
 * @param level Niveau d'indentation (commencer par 0)
 */
void print_directory_structure(const char *path, int level);

/**
 * Crée un nouveau projet à partir d'un modèle sélectionné
 * 
 * @param template_type Type de modèle à utiliser
 * @param project_path Chemin où créer le projet
 * @return EXIT_SUCCESS en cas de succès, EXIT_FAILURE en cas d'erreur
 */
int create_project_from_template(project_template_t template_type, const char *project_path);

/**
 * Arrête le serveur web en cours d'exécution
 * 
 * @return EXIT_SUCCESS si le serveur a été arrêté, EXIT_FAILURE sinon
 */
int stop_server(void);

/**
 * Analyse les arguments de la ligne de commande et exécute les commandes correspondantes
 * 
 * @param argc Nombre d'arguments
 * @param argv Tableau des arguments
 * @return EXIT_SUCCESS en cas de succès, EXIT_FAILURE en cas d'erreur
 */
int handle_cli_args(int argc, char *argv[]);

/**
 * Affiche l'aide de l'application
 */
void show_help(void);

#endif /* CLI_HANDLER_H */