# Guide du Développeur MKDF

Ce document fournit des informations techniques sur l'architecture interne de MKDF et comment contribuer au projet.

## Architecture du code

MKDF est organisé en plusieurs modules :

- **main.c** : Point d'entrée principal, analyse des arguments et dispatch
- **directory_handler.c** : Logique de création des structures de fichiers et répertoires
- **cli_handler.c** : Gestion de l'interface en ligne de commande interactive
- **web_handler.c** : Serveur web et gestion de l'interface utilisateur web

### Diagramme simplifié

```
main.c
  ├── directory_handler.c (création de structures)
  ├── cli_handler.c (interface CLI interactive)
  └── web_handler.c (serveur et interface web)
```

## Structure du projet

```
mkdf/
  ├── Makefile (compilation et installation)
  ├── include/ (fichiers d'en-tête .h)
  │   ├── directory_handler.h
  │   ├── cli_handler.h
  │   └── web_handler.h
  ├── src/ (fichiers sources .c)
  │   ├── main.c
  │   ├── directory_handler.c
  │   ├── cli_handler.c
  │   └── web_handler.c
  ├── web/ (fichiers de l'interface web)
  │   ├── index.html
  │   ├── styles.css
  │   └── css/
  │       └── girly.css
  ├── docs/ (documentation)
  └── build/ (fichiers de compilation)
```

## Modèles de projets disponibles

MKDF inclut plusieurs modèles de structures prédéfinis :

1. **Simple** : Structure minimaliste
2. **Multi-répertoires** : Structure élaborée
3. **Docker** : Configuration avec Docker
4. **FastAPI** : Structure pour API REST Python
5. **Vue+Vite** : Framework frontend
6. **Flask** : Application web Python
7. **React** : Application frontend React

Ces modèles sont définis comme des tableaux de chemins dans `directory_handler.c`.

## Algorithme d'expansion des accolades

L'expansion des accolades est gérée par un parseur récursif qui :
1. Identifie les sections entre accolades
2. Développe chaque option séparée par des virgules
3. Combine les résultats pour générer la liste complète des chemins

### Exemple de traitement

Pour l'entrée `projet/{src/{lib/,bin/},docs/}` :
1. Identification des sections entre accolades : `src/{lib/,bin/}` et `docs/`
2. Expansion récursive de `src/{lib/,bin/}` → `src/lib/` et `src/bin/`
3. Combinaison avec `docs/` pour obtenir `projet/src/lib/`, `projet/src/bin/`, `projet/docs/`

## Compilation et développement

### Prérequis

- GCC ou Clang
- Make
- Bibliothèque pthread

### Compiler pendant le développement

```bash
# Compilation avec informations de débogage
make

# Exécution du programme
./mkdf

# Lancement des tests (si disponibles)
make test
```

### Compilation pour la production

```bash
# Optimisation pour la production
make CFLAGS="-O2 -Wall -Wextra -pthread"
```

## Contribuer au projet

Si vous souhaitez contribuer à MKDF :

1. Créez une branche pour votre fonctionnalité
2. Écrivez votre code en suivant le style existant
3. Ajoutez des tests si nécessaire
4. Vérifiez que tout compile sans erreurs ou warnings
5. Soumettez une pull request

### Conventions de codage

- Indentation avec des tabulations
- Accolades sur la même ligne que les déclarations de fonctions
- Commentaires pour expliquer le code complexe
- Noms de fonctions en snake_case

---

## Navigation

- [Retour à l'index](index.md)
- Pages connexes :
  - [Installation](installation.md)
  - [Cas d'utilisation](use_cases.md)
- Documentation technique complète du projet