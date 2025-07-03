# MKDF - MaKeDir&Files

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-AGPL--3.0-green.svg)

MKDF is a powerful and flexible utility for creating directory and file structures. It is particularly useful for quickly initializing projects from predefined or custom templates.

> **⚠️ Note to developers:** The compilation of this project currently generates several warnings, mainly related to potential string truncation and signed/unsigned type comparisons. These warnings do not affect the functionality of the program, but we are looking for contributors to help resolve them. See the [Contributing](#contributing) section for more details.

## Features

- 🚀 Intuitive Command Line Interface (CLI)
- 💻 User-friendly web interface with structure preview
- 🔧 Creation of file structures with brace expansion
- 📦 Predefined project templates (React, Flask, FastAPI, Vue+Vite, etc.)
- 🛠️ Custom structures with expressive syntax
- 🏠 Support for tilde (~) expansion in paths

## Installation

For complete installation instructions, see the [Installation Guide](docs/EN/installation.md).

### From Source

```bash
git clone https://github.com/Noziop/mkdf.git
cd mkdf
./install.sh --EN  # English installation
./install.sh       # French installation (default)
```

The installation script will allow you to choose between:
- System installation (in /usr/local/bin, requires sudo)
- User installation (in ~/.local/bin)
- Installation in a custom directory

## Usage

### Command Line Mode

```bash
# Help and version
mkdf --help
mkdf --version

# Interactive mode
mkdf

# Create a structure with brace expansion
mkdf 'myproject/{src/{lib/,bin/,include/},docs/{user/,dev/},tests/,README.md,LICENSE}'

# Create a project from a template
mkdf --create my-project react
mkdf -c ~/projects/api-server fastapi
```

For complete documentation of the command line interface, see the [Command Line Usage Guide](docs/EN/cli_usage.md).

### Web Mode

```bash
# Start the web interface
mkdf --web
# or
make web
```

Then open your browser at the indicated address (usually http://localhost:8080).

For more information about the web interface, see the [Web Interface Guide](docs/EN/web_usage.md).

## Expansion Syntax

MKDF uses a brace expansion syntax to efficiently define complex structures:

- `{a,b,c}` creates a, b and c at the same level
- Paths ending with `/` are created as directories
- Others are created as empty files
- You can nest braces: `{a/{b,c},d}` creates a/b, a/c, and d

## Complete Documentation

All documentation is available in English and French:

### English Documentation

- [Documentation Index](docs/EN/index.md)
- [Installation Guide](docs/EN/installation.md)
- [Command Line Usage](docs/EN/cli_usage.md)
- [Web Interface](docs/EN/web_usage.md)
- [Project Templates](docs/EN/project_templates.md)
- [Use Cases](docs/EN/use_cases.md)
- [Developer Guide](docs/EN/developer_guide.md)

### Documentation Française

- [Index de la documentation](docs/FR/index.md)
- [Guide d'installation](docs/FR/installation.md)
- [Utilisation en ligne de commande](docs/FR/cli_usage.md)
- [Interface Web](docs/FR/web_usage.md)
- [Modèles de projets](docs/FR/project_templates.md)
- [Cas d'utilisation](docs/FR/use_cases.md)
- [Guide du développeur](docs/FR/developer_guide.md)

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0) - see the LICENSE file for details.

This free software license ensures that:
1. The code remains free and open source
2. All modifications must also be shared under the same license
3. Even when the software is offered as a network service, the source code must be made available
4. Commercial exploitation is subject to AGPL conditions

## Author

Developed by [Fassih Belmokhtar](https://github.com/Noziop)  
Contact: contact@fassih.ch

## Contributing

We are actively looking for contributors to help improve MKDF, especially to resolve the current compilation warnings:

### Current Warnings

```
gcc -Wall -Wextra -g -pthread -Iinclude -c src/cli_handler.c -o build/cli_handler.o
src/cli_handler.c: In function 'start_cli_mode':
src/cli_handler.c:993:58: warning: '%s' directive output may be truncated writing up to 4095 bytes into a region of size between 0 and 4095 [-Wformat-truncation=]
  993 |                         snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
      |                                                          ^~                ~~~~~~~~~~
src/cli_handler.c:993:25: note: 'snprintf' output between 2 and 8192 bytes into a destination of size 4096
  993 |                         snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
      |                         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/cli_handler.c:918:70: warning: '%s' directive output may be truncated writing up to 4095 bytes into a region of size between 0 and 4095 [-Wformat-truncation=]
  918 |                                     snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
      |                                                                      ^~                ~~~~~~~~~~
src/cli_handler.c:918:37: note: 'snprintf' output between 2 and 8192 bytes into a destination of size 4096
  918 |                                     snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
      |                                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/cli_handler.c:957:78: warning: '%s' directive output may be truncated writing up to 1023 bytes into a region of size between 0 and 4095 [-Wformat-truncation=]
  957 |                             snprintf(project_path, sizeof(project_path), "%s/%s", target_dir, project_name);
      |                                                                              ^~               ~~~~~~~~~~~~
src/cli_handler.c:957:29: note: 'snprintf' output between 2 and 5120 bytes into a destination of size 4096
  957 |                             snprintf(project_path, sizeof(project_path), "%s/%s", target_dir, project_name);
      |                             ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At top level:
src/cli_handler.c:1289:12: warning: 'handle_directory_change' defined but not used [-Wunused-function]
 1289 | static int handle_directory_change(char *current_dir, size_t current_dir_size __attribute__((unused)), char *target_dir, size_t target_dir_size) {
      |            ^~~~~~~~~~~~~~~~~~~~~~~
gcc -Wall -Wextra -g -pthread -Iinclude -c src/web_handler.c -o build/web_handler.o
src/web_handler.c: In function 'handle_client':
src/web_handler.c:189:23: warning: comparison of integer expressions of different signedness: 'ssize_t' {aka 'long int'} and 'size_t' {aka 'long unsigned int'} [-Wsign-compare]
  189 |     while (total_sent < response_len) {
      |                       ^
```

### How to Contribute

If you have C programming skills and would like to help improve MKDF:

1. **Resolve compilation warnings**: Propose fixes for the warnings listed above.
2. **Internationalization**: Help us implement a better structure for multilingual support.
3. **Code improvement**: Identify and fix potential issues or suggest enhancements.

To contribute:
1. Fork the project
2. Create a feature branch (`git checkout -b fix-warnings`)
3. Commit your changes (`git commit -am 'Fix format truncation warnings'`)
4. Push the branch (`git push origin fix-warnings`)
5. Open a Pull Request

We are also open to any suggestions to improve the project!