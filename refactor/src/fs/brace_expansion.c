#include "../include/fs/brace_expansion.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

/**
 * Initialise une structure BraceExpansion
 */
BraceExpansion init_brace_expansion(void) {
    BraceExpansion result;
    result.paths = NULL;
    result.count = 0;
    return result;
}

/**
 * Libère les ressources utilisées par une structure BraceExpansion
 */
void free_brace_expansion(BraceExpansion *expansion) {
    if (!expansion) return;
    
    for (size_t i = 0; i < expansion->count; i++) {
        free(expansion->paths[i]);
    }
    free(expansion->paths);
    
    expansion->paths = NULL;
    expansion->count = 0;
}

/**
 * Ajoute un chemin au résultat de l'expansion
 */
static int add_path_to_expansion(BraceExpansion *expansion, const char *path) {
    if (!expansion || !path) return -1;
    
    // Allouer ou réallouer le tableau de chemins
    char **new_paths = realloc(expansion->paths, (expansion->count + 1) * sizeof(char *));
    if (!new_paths) return -1;
    
    expansion->paths = new_paths;
    
    // Dupliquer le nouveau chemin
    expansion->paths[expansion->count] = strdup(path);
    if (!expansion->paths[expansion->count]) return -1;
    
    expansion->count++;
    return 0;
}

/**
 * Vérifie si un motif contient des accolades à expanser
 */
bool has_braces(const char *pattern) {
    if (!pattern) return false;
    
    // Recherche des accolades ouvrantes et fermantes
    const char *open_brace = strchr(pattern, '{');
    const char *close_brace = strchr(pattern, '}');
    
    // Il faut à la fois une accolade ouvrante et fermante,
    // et l'ouvrante doit apparaître avant la fermante
    if (open_brace && close_brace && open_brace < close_brace) {
        // Vérifier qu'il y a une virgule entre les accolades
        for (const char *p = open_brace + 1; p < close_brace; p++) {
            if (*p == ',') return true;
        }
    }
    
    return false;
}

/**
 * Trouve la prochaine paire d'accolades à traiter en priorité
 */
static int find_next_brace_pair(const char *pattern, size_t *start, size_t *end) {
    if (!pattern || !start || !end) return -1;
    
    const char *p = pattern;
    size_t depth = 0;
    size_t next_start = 0;
    bool found = false;
    
    // Parcourir le motif caractère par caractère
    for (size_t i = 0; p[i] != '\0'; i++) {
        if (p[i] == '{') {
            if (depth == 0) {
                next_start = i;
            }
            depth++;
        } 
        else if (p[i] == '}') {
            if (depth > 0) {
                depth--;
                if (depth == 0) {
                    *start = next_start;
                    *end = i;
                    found = true;
                    break;
                }
            }
        }
    }
    
    return found ? 0 : -1;
}

/**
 * Extrait les options d'une paire d'accolades
 */
static char** extract_options(const char *pattern, size_t start, size_t end, size_t *count) {
    if (!pattern || !count) return NULL;
    
    // +1 pour sauter l'accolade ouvrante, end-start-1 pour la longueur sans les accolades
    const char *content = pattern + start + 1;
    size_t content_len = end - start - 1;
    
    // Copier le contenu entre accolades
    char *temp = malloc(content_len + 1);
    if (!temp) return NULL;
    
    strncpy(temp, content, content_len);
    temp[content_len] = '\0';
    
    // Compter les virgules pour déterminer le nombre d'options
    size_t option_count = 1;
    for (size_t i = 0; i < content_len; i++) {
        if (temp[i] == ',' && (i == 0 || temp[i-1] != '\\')) {
            option_count++;
        }
    }
    
    // Allouer le tableau d'options
    char **options = malloc(option_count * sizeof(char *));
    if (!options) {
        free(temp);
        return NULL;
    }
    
    // Extraire chaque option
    char *token = strtok(temp, ",");
    size_t i = 0;
    
    while (token && i < option_count) {
        options[i] = strdup(token);
        if (!options[i]) {
            // Libérer la mémoire en cas d'erreur
            for (size_t j = 0; j < i; j++) {
                free(options[j]);
            }
            free(options);
            free(temp);
            return NULL;
        }
        token = strtok(NULL, ",");
        i++;
    }
    
    free(temp);
    *count = option_count;
    return options;
}

/**
 * Combine un préfixe, une option et un suffixe en un seul chemin
 */
static char* combine_path_parts(const char *prefix, const char *option, const char *suffix) {
    size_t prefix_len = prefix ? strlen(prefix) : 0;
    size_t option_len = option ? strlen(option) : 0;
    size_t suffix_len = suffix ? strlen(suffix) : 0;
    
    // Allouer la mémoire pour le chemin complet
    char *result = malloc(prefix_len + option_len + suffix_len + 1);
    if (!result) return NULL;
    
    // Copier les parties dans le chemin résultant
    result[0] = '\0';
    if (prefix) strcat(result, prefix);
    if (option) strcat(result, option);
    if (suffix) strcat(result, suffix);
    
    return result;
}

/**
 * Expande un motif contenant des accolades en multiples chemins
 */
int expand_braces(const char *pattern, BraceExpansion *result) {
    if (!pattern || !result) return -1;
    
    // Si le motif ne contient pas d'accolades, l'ajouter simplement au résultat
    if (!has_braces(pattern)) {
        return add_path_to_expansion(result, pattern);
    }
    
    // Trouver la prochaine paire d'accolades
    size_t start, end;
    if (find_next_brace_pair(pattern, &start, &end) != 0) {
        // Si pas de paire d'accolades valide, traiter comme un chemin simple
        return add_path_to_expansion(result, pattern);
    }
    
    // Extraire le préfixe et le suffixe
    char *prefix = NULL;
    char *suffix = NULL;
    
    if (start > 0) {
        prefix = malloc(start + 1);
        if (!prefix) return -1;
        
        strncpy(prefix, pattern, start);
        prefix[start] = '\0';
    }
    
    if (pattern[end + 1] != '\0') {
        suffix = strdup(pattern + end + 1);
        if (!suffix) {
            free(prefix);
            return -1;
        }
    }
    
    // Extraire les options entre accolades
    size_t option_count = 0;
    char **options = extract_options(pattern, start, end, &option_count);
    
    if (!options) {
        free(prefix);
        free(suffix);
        return -1;
    }
    
    // Pour chaque option, créer un nouveau motif et l'expanser récursivement
    for (size_t i = 0; i < option_count; i++) {
        // Combiner le préfixe, l'option et le suffixe
        char *new_pattern = combine_path_parts(prefix, options[i], suffix);
        if (!new_pattern) continue;
        
        // Expanser récursivement
        expand_braces(new_pattern, result);
        
        free(new_pattern);
    }
    
    // Nettoyer
    for (size_t i = 0; i < option_count; i++) {
        free(options[i]);
    }
    free(options);
    free(prefix);
    free(suffix);
    
    return 0;
}
