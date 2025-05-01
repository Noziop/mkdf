# Utilisation de la ligne de commande MKDF

Ce guide détaille toutes les commandes et options disponibles pour utiliser MKDF en ligne de commande.

## Syntaxe de base

La syntaxe générale de MKDF est la suivante :

```bash
mkdf [options] expression
```

Où `expression` est un chemin ou une expression utilisant la syntaxe d'expansion de MKDF.

## Syntaxe d'expansion

MKDF utilise une syntaxe puissante d'expansion avec des accolades pour définir la structure de répertoires et de fichiers.

### Exemple simple

```bash
mkdf 'projet/{src/,docs/,tests/}'
```

Cela créera la structure :

```
projet/
├── src/
├── docs/
└── tests/
```

### Imbrication

Vous pouvez imbriquer les accolades pour créer des structures plus complexes :

```bash
mkdf 'projet/{src/{models/,views/,controllers/},docs/,tests/{unit/,integration/}}'
```

Cela créera :

```
projet/
├── src/
│   ├── models/
│   ├── views/
│   └── controllers/
├── docs/
└── tests/
    ├── unit/
    └── integration/
```

### Création de fichiers

Pour créer des fichiers, omettez simplement la barre oblique à la fin du nom :

```bash
mkdf 'projet/{README.md,src/,docs/USAGE.md}'
```

Cela créera :

```
projet/
├── README.md
├── src/
└── docs/
    └── USAGE.md
```

### Utilisation de templates pour les fichiers

Pour créer des fichiers avec un contenu prédéfini, vous pouvez utiliser la syntaxe de template. Cette fonctionnalité permet de spécifier un fichier source (template) qui sera copié à l'emplacement de destination.

Syntaxe :
```bash
mkdf 'projet/{fichier-destination.ext:chemin/vers/fichier-template.ext}'
```

Exemple :
```bash
mkdf 'mon-projet/{README.md:/home/user/templates/readme-template.md}'
```

Cela créera le fichier `mon-projet/README.md` avec le contenu du fichier `/home/user/templates/readme-template.md`.

Vous pouvez combiner cette fonctionnalité avec les autres syntaxes d'expansion :
```bash
mkdf 'mon-projet/{README.md:/home/user/templates/readme.md,config.json:/home/user/templates/config.json,src/,docs/}'
```

Cela créera :
```
mon-projet/
├── README.md (contenu du template)
├── config.json (contenu du template) 
├── src/
└── docs/
```

### Plusieurs éléments au même niveau

Vous pouvez spécifier plusieurs éléments au même niveau en les séparant par des virgules :

```bash
mkdf 'projet/{src/,LICENSE,README.md,tests/}'
```

## Options principales

### Mode verbeux

```bash
mkdf -v 'mon-projet/{src/,docs/}'
# ou
mkdf --verbose 'mon-projet/{src/,docs/}'
```

Affiche les détails de chaque opération lors de la création des répertoires et des fichiers.

### Aide

```bash
mkdf -h
# ou
mkdf --help
```

Affiche l'aide et les options disponibles.

### Version

```bash
mkdf --version
```

Affiche la version actuelle de MKDF.

### Créer à partir d'un modèle

```bash
mkdf -c mon-projet react
# ou
mkdf --create mon-projet flask
```

Crée un nouveau projet basé sur un modèle prédéfini. Les modèles disponibles sont :

- `simple` : Structure minimale
- `multi` : Structure multi-répertoires
- `docker` : Projet avec configuration Docker
- `fastapi` : Application FastAPI
- `vue-vite` : Projet Vue.js avec Vite
- `flask` : Application Flask
- `react` : Application React

### Mode interactif

```bash
mkdf -i
# ou
mkdf --interactive
```

Lance MKDF en mode interactif, où vous pouvez entrer des expressions et voir les résultats en temps réel.

### Mode web

```bash
mkdf -w
# ou
mkdf --web
```

Lance l'interface web de MKDF, accessible par défaut à l'adresse http://localhost:8080.

### Port spécifique pour le mode web

```bash
mkdf -w -p 3000
# ou
mkdf --web --port 3000
```

Lance l'interface web sur un port spécifique.

### Mode silencieux

```bash
mkdf -q 'mon-projet/{src/,docs/}'
# ou
mkdf --quiet 'mon-projet/{src/,docs/}'
```

Supprime tous les messages de sortie.

### Mode simulation

```bash
mkdf -s 'mon-projet/{src/,docs/}'
# ou
mkdf --simulate 'mon-projet/{src/,docs/}'
```

Simule la création des répertoires et des fichiers sans les créer réellement.

### Force

```bash
mkdf -f 'mon-projet/{src/,docs/}'
# ou
mkdf --force 'mon-projet/{src/,docs/}'
```

Force la création même si les répertoires existent déjà.

## Exemples d'utilisation

### Exemple 1 : Projet web basique

```bash
mkdf 'mon-site/{css/,js/,img/,index.html,README.md}'
```

### Exemple 2 : Structure d'application Django

```bash
mkdf 'mon-app/{app/{models/,views/,templates/,static/},config/,requirements.txt,manage.py,README.md}'
```

### Exemple 3 : Structure pour un package Python

```bash
mkdf 'mon-package/{mon_package/{__init__.py,core.py,utils.py},tests/,setup.py,README.md,LICENSE}'
```

### Exemple 4 : Projet de recherche

```bash
mkdf 'recherche/{donnees/{brut/,traitees/},analyse/{scripts/,notebooks/},resultats/{figures/,tableaux/},rapport.md,biblio.bib}'
```

### Exemple 5 : Structure de documentation

```bash
mkdf 'documentation/{introduction.md,installation.md,api/{endpoints.md,auth.md},exemples/,faq.md}'
```

## Utilisation avancée

### Avec des chemins absolus

```bash
mkdf '/chemin/absolu/{src/,docs/,tests/}'
```

### Avec des chemins relatifs au répertoire utilisateur

```bash
mkdf '~/projets/nouveau-projet/{src/,docs/}'
```

### Combinaison avec d'autres commandes

```bash
# Créer une structure et initialiser Git
mkdf 'nouveau-projet/{src/,docs/,tests/}' && cd nouveau-projet && git init
```

### Redirection de la sortie

```bash
# Enregistrer la structure créée dans un fichier
mkdf -v 'mon-projet/{src/,docs/}' > structure.log
```

---

## Navigation

- [Retour à l'index](index.md)
- Page précédente : [Guide d'installation](installation.md)
- Pages suivantes : 
  - [Interface Web](web_usage.md)
  - [Modèles de projets](project_templates.md)