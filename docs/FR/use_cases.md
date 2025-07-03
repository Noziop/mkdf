# Cas d'utilisation de MKDF

Ce document présente différents scénarios d'utilisation de MKDF pour vous aider à tirer le meilleur parti de cet outil.

## Initialisation rapide de projets

MKDF est particulièrement utile pour initialiser rapidement de nouveaux projets sans avoir à créer manuellement tous les fichiers et répertoires.

### Exemple : Démarrer un projet microservice

```bash
# Créer une structure de base pour un microservice
mkdf 'my-service/{src/{controllers/,models/,services/,utils/},config/{dev/,prod/},tests/{unit/,integration/},docker/,docs/,README.md,Dockerfile,docker-compose.yml}'
```

### Exemple : Projet de documentation technique

```bash
# Créer une structure pour de la documentation technique
mkdf 'technical-docs/{overview/,architecture/{diagrams/,patterns/},api/{endpoints/,models/,authentication/},deployment/{local/,staging/,production/},examples/,images/,index.md,README.md}'
```

## Création de structures pour le développement web

### Projet frontend moderne

```bash
# Structure pour un projet frontend avec composants, routes, styles, etc.
mkdf 'webapp/{src/{components/{common/,layout/,forms/,pages/},hooks/,utils/,styles/{base/,components/,themes/},assets/{images/,icons/,fonts/}},public/{index.html,favicon.ico},tests/,package.json,README.md}'
```

### API Backend

```bash
# Structure pour une API backend
mkdf 'api-server/{src/{controllers/,models/,middleware/{auth/,validation/,error/},services/,utils/},config/{env/,database/},tests/,docs/,logs/,README.md}'
```

## Création de structures pour la data science

```bash
# Projet d'analyse de données
mkdf 'data-analysis/{data/{raw/,processed/,external/},notebooks/,src/{preprocessing/,features/,models/,visualization/},reports/{figures/,tables/},requirements.txt,README.md}'
```

## Organisation de petits projets personnels

```bash
# Structure pour un projet personnel
mkdf '~/projects/side-project/{code/,notes/,resources/,ideas.md,todo.md,README.md}'
```

## Utilisation dans des scripts

MKDF peut être intégré dans des scripts pour automatiser la création de structures de projets personnalisées :

```bash
#!/bin/bash
# Script pour initialiser un nouveau projet web

project_name=$1

if [ -z "$project_name" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

# Créer la structure de base avec MKDF
mkdf "$project_name/{frontend/{src/{components/,pages/,assets/},public/,package.json},backend/{src/,tests/,config/},docs/,README.md}"

# Initialiser git
cd "$project_name"
git init
echo "node_modules/" > .gitignore
echo "*.log" >> .gitignore

echo "Projet $project_name créé avec succès!"
```

## Combinaison avec d'autres outils

### Avec Git

```bash
# Créer un projet et l'initialiser avec Git
mkdf 'new-project/{src/,tests/,README.md,LICENSE}' && cd new-project && git init
```

### Avec npm/yarn

```bash
# Créer un projet JavaScript et initialiser npm
mkdf 'js-app/{src/{components/,utils/},tests/,README.md}' && cd js-app && npm init -y
```

## Exemples de structures complexes

### Application complète full-stack

```bash
mkdf 'myapp/{backend/{src/{controllers/,models/,routes/,services/,utils/,middlewares/},tests/{unit/,integration/,e2e/},config/,docs/,package.json},frontend/{src/{components/,pages/,services/,assets/},public/,tests/,package.json},docs/,docker/,scripts/,README.md}'
```

### Projet avec plusieurs services

```bash
mkdf 'microservices/{auth-service/{src/,tests/,Dockerfile},user-service/{src/,tests/,Dockerfile},notification-service/{src/,tests/,Dockerfile},api-gateway/{src/,configs/},docker-compose.yml,README.md}'
```

---

## Navigation

- [Retour à l'index](index.md)
- Pages connexes :
  - [Modèles de projets](project_templates.md)
  - [Utilisation en ligne de commande](cli_usage.md)
- [Guide du développeur](developer_guide.md) - Pour contribuer au projet