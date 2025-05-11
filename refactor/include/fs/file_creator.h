#ifndef FILE_CREATOR_H
#define FILE_CREATOR_H

#include <stdbool.h>
#include <stddef.h>

/**
 * Crée un fichier vide à l'emplacement spécifié
 *
 * @param path Chemin du fichier à créer
 * @return 0 si succès, -1 si erreur
 */
int create_empty_file(const char *path, bool force);

/**
 * Crée un fichier à partir d'un template
 *
 * @param path Chemin du fichier à créer
 * @param template_path Chemin du template à utiliser
 * @return 0 si succès, -1 si erreur
 */
int create_file_from_template(const char *path, const char *template_path);

/**
 * Fonction principale pour créer un fichier
 * Analyse le chemin et détermine s'il faut utiliser un template ou non
 *
 * @param path Chemin du fichier (peut contenir un template après ":")
 * @param force Écraser si le fichier existe déjà
 * @return 0 si succès, -1 si erreur
 */
int create_file(const char *path, bool force);

/**
 * Vérifie si un fichier existe
 *
 * @param path Chemin du fichier à vérifier
 * @return true si le fichier existe, false sinon
 */
bool file_exists(const char *path);

#endif /* FILE_CREATOR_H */
