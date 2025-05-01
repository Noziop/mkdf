# MKDF Use Cases

This document presents various usage scenarios for MKDF to help you get the most out of this tool.

## Quick Project Initialization

MKDF is particularly useful for quickly initializing new projects without having to manually create all files and directories.

### Example: Starting a Microservice Project

```bash
# Create a basic structure for a microservice
mkdf 'my-service/{src/{controllers/,models/,services/,utils/},config/{dev/,prod/},tests/{unit/,integration/},docker/,docs/,README.md,Dockerfile,docker-compose.yml}'
```

### Example: Technical Documentation Project

```bash
# Create a structure for technical documentation
mkdf 'technical-docs/{overview/,architecture/{diagrams/,patterns/},api/{endpoints/,models/,authentication/},deployment/{local/,staging/,production/},examples/,images/,index.md,README.md}'
```

## Creating Structures for Web Development

### Modern Frontend Project

```bash
# Structure for a frontend project with components, routes, styles, etc.
mkdf 'webapp/{src/{components/{common/,layout/,forms/,pages/},hooks/,utils/,styles/{base/,components/,themes/},assets/{images/,icons/,fonts/}},public/{index.html,favicon.ico},tests/,package.json,README.md}'
```

### Backend API

```bash
# Structure for a backend API
mkdf 'api-server/{src/{controllers/,models/,middleware/{auth/,validation/,error/},services/,utils/},config/{env/,database/},tests/,docs/,logs/,README.md}'
```

## Creating Structures for Data Science

```bash
# Data analysis project
mkdf 'data-analysis/{data/{raw/,processed/,external/},notebooks/,src/{preprocessing/,features/,models/,visualization/},reports/{figures/,tables/},requirements.txt,README.md}'
```

## Organizing Small Personal Projects

```bash
# Structure for a personal project
mkdf '~/projects/side-project/{code/,notes/,resources/,ideas.md,todo.md,README.md}'
```

## Using MKDF in Scripts

MKDF can be integrated into scripts to automate the creation of custom project structures:

```bash
#!/bin/bash
# Script to initialize a new web project

project_name=$1

if [ -z "$project_name" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

# Create the basic structure with MKDF
mkdf "$project_name/{frontend/{src/{components/,pages/,assets/},public/,package.json},backend/{src/,tests/,config/},docs/,README.md}"

# Initialize git
cd "$project_name"
git init
echo "node_modules/" > .gitignore
echo "*.log" >> .gitignore

echo "Project $project_name successfully created!"
```

## Combining with Other Tools

### With Git

```bash
# Create a project and initialize it with Git
mkdf 'new-project/{src/,tests/,README.md,LICENSE}' && cd new-project && git init
```

### With npm/yarn

```bash
# Create a JavaScript project and initialize npm
mkdf 'js-app/{src/{components/,utils/},tests/,README.md}' && cd js-app && npm init -y
```

## Examples of Complex Structures

### Complete Full-Stack Application

```bash
mkdf 'myapp/{backend/{src/{controllers/,models/,routes/,services/,utils/,middlewares/},tests/{unit/,integration/,e2e/},config/,docs/,package.json},frontend/{src/{components/,pages/,services/,assets/},public/,tests/,package.json},docs/,docker/,scripts/,README.md}'
```

### Project with Multiple Services

```bash
mkdf 'microservices/{auth-service/{src/,tests/,Dockerfile},user-service/{src/,tests/,Dockerfile},notification-service/{src/,tests/,Dockerfile},api-gateway/{src/,configs/},docker-compose.yml,README.md}'
```

---

## Navigation

- [Back to Index](index.md)
- Related pages:
  - [Project Templates](project_templates.md)
  - [Command Line Usage](cli_usage.md)
- [Developer Guide](developer_guide.md) - For contributing to the project