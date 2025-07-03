#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <libgen.h>
#include "../include/directory_handler.h"
#include "../include/cli_handler.h"
#include "../include/web_handler.h"

#define VERSION "1.0.0"

/**
 * Fonction pour nettoyer les caractères d'échappement dans les chaînes d'entrée
 */
static char* clean_path_input(const char* input) {
    if (!input) return NULL;
    
    size_t len = strlen(input);
    char* cleaned = (char*)malloc(len + 1);
    if (!cleaned) return NULL;
    
    size_t i, j = 0;
    for (i = 0; i < len; i++) {
        if (input[i] == '\\' && i + 1 < len) {
            // Séquence d'échappement trouvée
            i++; // Passer au caractère échappé
            cleaned[j++] = input[i];
        } else {
            cleaned[j++] = input[i];
        }
    }
    cleaned[j] = '\0';
    
    return cleaned;
}

void print_usage(void) {
    printf("Usage:\n");
    printf("  mkdf 'pattern_with_{braces}'          - Create directory structure with brace expansion\n");
    printf("  mkdf project/subdirectory/etc         - Create specific paths\n");
    printf("  mkdf                                  - Interactive CLI mode\n");
    printf("  mkdf --web                            - Start web interface\n");
    printf("  mkdf --help                           - Show this help\n");
    printf("  mkdf --version                        - Show version\n");
    printf("  mkdf -s [pattern]                     - Simulate creation (no actual changes made)\n");
    printf("  mkdf -i                               - Interactive mode\n");
    printf("  mkdf -f [pattern]                     - Force creation (overwrite existing files)\n");
    printf("  mkdf -q [pattern]                     - Quiet mode (no output)\n");
    printf("\nExamples:\n");
    printf("  mkdf 'myproject/{backend/{app/{api/{v1/endpoints/{users,feature1,feature2}.py,router/{deps,router}.py},service/,models/,utils/,main.py},frontend/{src/{components/,store/,router/,views/,App.vue,main.js},package.json,vite.config.js}'\n");
    printf("  mkdf project/{src/{components/,views/},docs/,README.md}\n");
    printf("\nNote: Paths ending with / will be created as directories, otherwise as files.\n");
    printf("\nIMPORTANT: When using braces, always enclose the pattern in single quotes (') to prevent shell expansion.\n");
}

// Point d'entrée principal du programme
int main(int argc, char *argv[]) {
    // This function is only for demonstration of escape sequence processing
    // and could be used in future versions, so we'll mark it as potentially useful
    (void)clean_path_input; // Suppress unused function warning
    
    return handle_cli_args(argc, argv);
}