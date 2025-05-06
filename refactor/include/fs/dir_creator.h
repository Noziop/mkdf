#ifndef DIR_CREATOR_H
#define DIR_CREATOR_H

#include <stdbool.h>
#include <stddef.h>

/**
 * Crée un répertoire à l'emplacement spécifié
 * (Équivalent à mkdir simple)
 *
 * @param path Chemin du répertoire à créer
 * @return 0 si succès, -1 si erreur
 */
int create_directory(const char *path);

/**
 * Crée un répertoire et tous ses parents si nécessaire
 * (Équivalent à mkdir -p)
 *
 * @param path Chemin du répertoire à créer
 * @return 0 si succès, -1 si erreur
 */
int create_directory_recursive(const char *path);

/**
 * Crée une structure de répertoires d'après un chemin expansé
 * (Sans expansion d'accolades - utilise brace_expansion.h pour cela)
 *
 * @param path Chemin du répertoire à créer
 * @param force Écraser si existe déjà
 * @return 0 si succès, -1 si erreur
 */
int create_directory_structure(const char *path, bool force);

/**
 * Vérifie si un répertoire existe
 *
 * @param path Chemin du répertoire à vérifier
 * @return true si le répertoire existe, false sinon
 */
bool directory_exists(const char *path);

#endif /* DIR_CREATOR_H */
