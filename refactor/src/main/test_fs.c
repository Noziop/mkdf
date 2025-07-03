#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "../../include/fs/brace_expansion.h"
#include "../../include/fs/dir_creator.h"
#include "../../include/fs/file_creator.h"
#include "../../include/fs/path_analyzer.h"

int main() {
    const char *pattern = "test/{src/,docs/,README.md}";
    printf("Testing brace expansion for pattern: %s\n", pattern);

    BraceExpansion expansion = init_brace_expansion();
    if (expand_braces(pattern, &expansion) != 0) {
        fprintf(stderr, "Brace expansion failed\n");
        return 1;
    }

    printf("Expanded paths (%zu):\n", expansion.count);
    for (size_t i = 0; i < expansion.count; i++) {
        printf("  %zu: %s\n", i + 1, expansion.paths[i]);
        if (is_directory_path(expansion.paths[i])) {
            printf("    Creating directory: %s\n", expansion.paths[i]);
            if (create_directory_recursive(expansion.paths[i], false) != 0) {
                fprintf(stderr, "Failed to create directory %s\n", expansion.paths[i]);
            }
        } else {
            printf("    Creating file: %s\n", expansion.paths[i]);
            if (create_empty_file(expansion.paths[i], false) != 0) {
                fprintf(stderr, "Failed to create file %s\n", expansion.paths[i]);
            }
        }
    }

    free_brace_expansion(&expansion);
    return 0;
}
