#ifndef WEB_HANDLER_H
#define WEB_HANDLER_H

/**
 * Démarre l'interface web sur http://localhost:8080
 * 
 * @return EXIT_SUCCESS si le serveur a démarré correctement, EXIT_FAILURE sinon
 */
int start_web_interface(void);

/**
 * Démarre l'interface web sur le port spécifié
 * 
 * @param port Le port à utiliser pour l'interface web
 * @return EXIT_SUCCESS si le serveur a démarré correctement, EXIT_FAILURE sinon
 */
int start_web_interface_with_port(int port);

/**
 * Arrête l'interface web si elle est en cours d'exécution
 * 
 * @return EXIT_SUCCESS si le serveur a été arrêté correctement, EXIT_FAILURE sinon
 */
int stop_web_interface(void);

/**
 * Traite une requête HTTP et génère une réponse
 * 
 * @param request La requête HTTP à traiter
 * @param response Le buffer où stocker la réponse
 * @return 0 en cas de succès, -1 sinon
 */
int handle_web_request(const char *request, char *response);

/**
 * Crée un projet à partir d'un template prédéfini
 *
 * @param path Le chemin où créer le projet
 * @return EXIT_SUCCESS en cas de succès, EXIT_FAILURE sinon
 */
int create_template_project(const char *path);

/**
 * Liste le contenu d'un répertoire et le renvoie en format JSON
 *
 * @param path Le chemin du répertoire à lister
 * @param response Le buffer où stocker la réponse JSON
 * @return 0 en cas de succès, -1 sinon
 */
int list_directory(const char *path, char *response);

/**
 * Gère la connexion d'un client web
 * 
 * @param arg Les arguments pour la connexion du client
 * @return NULL
 */
void *handle_client(void *arg);

#endif /* WEB_HANDLER_H */