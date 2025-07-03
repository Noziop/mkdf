# MKDF Command Line Usage

This guide details all the commands and options available for using MKDF from the command line.

## Basic Syntax

The general syntax of MKDF is as follows:

```bash
mkdf [options] expression
```

Where `expression` is a path or an expression using MKDF's expansion syntax.

## Expansion Syntax

MKDF uses a powerful brace expansion syntax to define the directory and file structure.

### Simple Example

```bash
mkdf 'project/{src/,docs/,tests/}'
```

This will create the structure:

```
project/
├── src/
├── docs/
└── tests/
```

### Nesting

You can nest braces to create more complex structures:

```bash
mkdf 'project/{src/{models/,views/,controllers/},docs/,tests/{unit/,integration/}}'
```

This will create:

```
project/
├── src/
│   ├── models/
│   ├── views/
│   └── controllers/
├── docs/
└── tests/
    ├── unit/
    └── integration/
```

### Creating Files

To create files, simply omit the trailing slash:

```bash
mkdf 'project/{README.md,src/,docs/USAGE.md}'
```

This will create:

```
project/
├── README.md
├── src/
└── docs/
    └── USAGE.md
```

### Using File Templates

To create files with predefined content, you can use the template syntax. This feature allows you to specify a source file (template) that will be copied to the destination location.

Syntax:
```bash
mkdf 'project/{destination-file.ext:/path/to/template-file.ext}'
```

Example:
```bash
mkdf 'my-project/{README.md:/home/user/templates/readme-template.md}'
```

This will create the file `my-project/README.md` with the content of the file `/home/user/templates/readme-template.md`.

You can combine this feature with other expansion syntaxes:
```bash
mkdf 'my-project/{README.md:/home/user/templates/readme.md,config.json:/home/user/templates/config.json,src/,docs/}'
```

This will create:
```
my-project/
├── README.md (with template content)
├── config.json (with template content)
├── src/
└── docs/
```

### Multiple Items at the Same Level

You can specify multiple items at the same level by separating them with commas:

```bash
mkdf 'project/{src/,LICENSE,README.md,tests/}'
```

## Main Options

### Verbose Mode

```bash
mkdf -v 'my-project/{src/,docs/}'
# or
mkdf --verbose 'my-project/{src/,docs/}'
```

Displays details of each operation when creating directories and files.

### Help

```bash
mkdf -h
# or
mkdf --help
```

Displays help and available options.

### Version

```bash
mkdf --version
```

Displays the current version of MKDF.

### Create from Template

```bash
mkdf -c my-project react
# or
mkdf --create my-project flask
```

Creates a new project based on a predefined template. Available templates are:

- `simple`: Minimal structure
- `multi`: Multi-directory structure
- `docker`: Project with Docker configuration
- `fastapi`: FastAPI application
- `vue-vite`: Vue.js project with Vite
- `flask`: Flask application
- `react`: React application

### Interactive Mode

```bash
mkdf -i
# or
mkdf --interactive
```

Launches MKDF in interactive mode, where you can enter expressions and see results in real-time.

### Web Mode

```bash
mkdf -w
# or
mkdf --web
```

Launches the MKDF web interface, accessible by default at http://localhost:8080.

### Specific Port for Web Mode

```bash
mkdf -w -p 3000
# or
mkdf --web --port 3000
```

Launches the web interface on a specific port.

### Quiet Mode

```bash
mkdf -q 'my-project/{src/,docs/}'
# or
mkdf --quiet 'my-project/{src/,docs/}'
```

Suppresses all output messages.

### Simulation Mode

```bash
mkdf -s 'my-project/{src/,docs/}'
# or
mkdf --simulate 'my-project/{src/,docs/}'
```

Simulates creating directories and files without actually creating them.

### Force

```bash
mkdf -f 'my-project/{src/,docs/}'
# or
mkdf --force 'my-project/{src/,docs/}'
```

Forces creation even if directories already exist.

## Usage Examples

### Example 1: Basic Web Project

```bash
mkdf 'my-site/{css/,js/,img/,index.html,README.md}'
```

### Example 2: Django Application Structure

```bash
mkdf 'my-app/{app/{models/,views/,templates/,static/},config/,requirements.txt,manage.py,README.md}'
```

### Example 3: Python Package Structure

```bash
mkdf 'my-package/{my_package/{__init__.py,core.py,utils.py},tests/,setup.py,README.md,LICENSE}'
```

### Example 4: Research Project

```bash
mkdf 'research/{data/{raw/,processed/},analysis/{scripts/,notebooks/},results/{figures/,tables/},report.md,biblio.bib}'
```

### Example 5: Documentation Structure

```bash
mkdf 'documentation/{introduction.md,installation.md,api/{endpoints.md,auth.md},examples/,faq.md}'
```

## Advanced Usage

### With Absolute Paths

```bash
mkdf '/absolute/path/{src/,docs/,tests/}'
```

### With Paths Relative to User Directory

```bash
mkdf '~/projects/new-project/{src/,docs/}'
```

### Combination with Other Commands

```bash
# Create a structure and initialize Git
mkdf 'new-project/{src/,docs/,tests/}' && cd new-project && git init
```

### Output Redirection

```bash
# Save the created structure to a file
mkdf -v 'my-project/{src/,docs/}' > structure.log
```

---

## Navigation

- [Back to Index](index.md)
- Previous page: [Installation Guide](installation.md)
- Next pages: 
  - [Web Interface](web_usage.md)
  - [Project Templates](project_templates.md)