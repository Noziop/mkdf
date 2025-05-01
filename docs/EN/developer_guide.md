# MKDF Developer Guide

This document provides technical information about MKDF's internal architecture and how to contribute to the project.

## Code Architecture

MKDF is organized into several modules:

- **main.c**: Main entry point, argument parsing and dispatch
- **directory_handler.c**: Logic for creating file and directory structures
- **cli_handler.c**: Management of the interactive command-line interface
- **web_handler.c**: Web server and web user interface management

### Simplified Diagram

```
main.c
  ├── directory_handler.c (structure creation)
  ├── cli_handler.c (interactive CLI interface)
  └── web_handler.c (web server and interface)
```

## Project Structure

```
mkdf/
  ├── Makefile (compilation and installation)
  ├── include/ (header files .h)
  │   ├── directory_handler.h
  │   ├── cli_handler.h
  │   └── web_handler.h
  ├── src/ (source files .c)
  │   ├── main.c
  │   ├── directory_handler.c
  │   ├── cli_handler.c
  │   └── web_handler.c
  ├── web/ (web interface files)
  │   ├── index.html
  │   ├── styles.css
  │   └── css/
  │       └── girly.css
  ├── docs/ (documentation)
  └── build/ (compilation files)
```

## Available Project Templates

MKDF includes several predefined structure templates:

1. **Simple**: Minimalist structure
2. **Multi-directory**: Elaborate structure
3. **Docker**: Configuration with Docker
4. **FastAPI**: Structure for Python REST API
5. **Vue+Vite**: Frontend framework
6. **Flask**: Python web application
7. **React**: React frontend application

These templates are defined as path arrays in `directory_handler.c`.

## Brace Expansion Algorithm

Brace expansion is handled by a recursive parser that:
1. Identifies sections between braces
2. Expands each option separated by commas
3. Combines the results to generate the complete list of paths

### Processing Example

For the input `project/{src/{lib/,bin/},docs/}`:
1. Identification of sections between braces: `src/{lib/,bin/}` and `docs/`
2. Recursive expansion of `src/{lib/,bin/}` → `src/lib/` and `src/bin/`
3. Combination with `docs/` to get `project/src/lib/`, `project/src/bin/`, `project/docs/`

## Compilation and Development

### Prerequisites

- GCC or Clang
- Make
- pthread library

### Compiling during Development

```bash
# Compilation with debugging information
make

# Running the program
./mkdf

# Running tests (if available)
make test
```

### Production Compilation

```bash
# Optimization for production
make CFLAGS="-O2 -Wall -Wextra -pthread"
```

## Contributing to the Project

If you wish to contribute to MKDF:

1. Create a branch for your feature
2. Write your code following the existing style
3. Add tests if necessary
4. Verify that everything compiles without errors or warnings
5. Submit a pull request

### Coding Conventions

- Indentation with tabs
- Braces on the same line as function declarations
- Comments to explain complex code
- Function names in snake_case

---

## Navigation

- [Back to Index](index.md)
- Related pages:
  - [Installation Guide](installation.md)
  - [Use Cases](use_cases.md)
- Complete Technical Documentation