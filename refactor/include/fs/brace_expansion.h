#ifndef BRACE_EXPANSION_H
#define BRACE_EXPANSION_H

#include <stdbool.h>
#include <stddef.h>
#include <stdbool.h>  // Ajouté
#include <stddef.h>   // Ajouté
#include <stdlib.h>   // Ajouté
#include <string.h>   // Ajouté

/**
 * Structure pour stocker le résultat de l'expansion d'accolades
 */
typedef struct {
    char **paths;    // Tableau de chemins expansés
    size_t count;    // Nombre de chemins dans le tableau
} BraceExpansion;

/**
 * Initialise une structure BraceExpansion
 *
 * @return Structure initialisée
 */
BraceExpansion init_brace_expansion(void);

/**
 * Expande un motif contenant des accolades en multiples chemins
 *
 * @param pattern Le motif à expanser (ex: "dir/{a,b}/file.txt")
 * @param result Pointeur vers une structure BraceExpansion pour stocker le résultat
 * @return 0 si succès, -1 si erreur
 */
int expand_braces(const char *pattern, BraceExpansion *result);

/**
 * Vérifie si un motif contient des accolades à expanser
 *
 * @param pattern Le motif à vérifier
 * @return true si le motif contient des accolades, false sinon
 */
bool has_braces(const char *pattern);

/**
 * Libère les ressources utilisées par une structure BraceExpansion
 *
 * @param expansion Pointeur vers la structure à libérer
 */
void free_brace_expansion(BraceExpansion *expansion);

#endif /* BRACE_EXPANSION_H */
