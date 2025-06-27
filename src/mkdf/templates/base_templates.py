def get_simple_template():
    return {
        'README.md': '# Simple Project',
        'src/': None
    }

def get_low_level_template():
    return {
        'src/': {
            'main.c': '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}'
        },
        'include/': None,
        'lib/': None,
        'Makefile': 'all:\n\tgcc src/main.c -o main'
    }
