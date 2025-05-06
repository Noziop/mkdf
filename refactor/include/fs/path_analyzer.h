#ifndef PATH_ANALYZER_H
#define PATH_ANALYZER_H

#include <stdbool.h>
#include <stddef.h>

/**
 * Détermine si un chemin correspond à un répertoire
 * 
 * @param path Le chemin à analyser
 * @return true si c'est un répertoire, false sinon
 */
bool is_directory_path(const char *path);

/**
 * Détermine si un chemin correspond à un fichier
 * 
 * @param path Le chemin à analyser
 * @return true si c'est un fichier, false sinon
 */
bool is_file_path(const char *path);

/**
 * Vérifie si un chemin se trouve dans le home directory
 * 
 * @param path Le chemin à vérifier
 * @return true si dans le home, false sinon
 */
bool is_path_in_home_directory(const char *path);

/**
 * Expande le tilde (~) dans un chemin
 * 
 * @param path Chemin avec tilde
 * @param expanded_path Buffer pour le résultat
 * @param size Taille du buffer
 * @return 0 si succès, -1 si erreur
 */
int expand_tilde(const char *path, char *expanded_path, size_t size);

/**
 * Vérifie si un chemin utilise un template (format fichier.txt:/chemin/vers/template.txt)
 * 
 * @param path Le chemin à vérifier
 * @return true si c'est un template, false sinon
 */
bool is_template_path(const char *path);

/**
 * Extrait les infos d'un chemin template
 * 
 * @param path Le chemin complet
 * @param dest_path Buffer pour le chemin destination
 * @param template_path Buffer pour le chemin du template
 * @param size Taille des buffers
 * @return 0 si succès, -1 si erreur
 */
int extract_template_info(const char *path, char *dest_path, char *template_path, size_t size);

#endif /* PATH_ANALYZER_H */
