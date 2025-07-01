# MKDF – Make Directories and Files

Cherish your git flow or perish!

```
![Poetry](https://img.shields.io/badge/Poetry-managed-blueviolet?style=for-the-badge&logo=pythonields.io/badge/Python-3.10%2B-blue?style=for-the-badge://img.shields.io/badge/FastAPI-async-green?style=for-the-badge&logo=fastapiields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge://img.shields.io/badge/SQLite-embedded-003B57?style=for Source](https://img.shields.io/badge/Open%20Source-🌍-brightgreen?style=for-the-badge git flow or perish!](https://img.shields.io/badge/Cherish%20your%20git%20flow%20or%20perish!-blueviolet?style=for-the-badge -rf *](https://img.shields.io/badge/SURVIVED--rm--rf--*-critical?style=for-the-badge&logo=linux&logoColor=white://img.shields.io/badge/coverage-34%25-yellow?style=for-the-badge MKDF ?

MKDF est un générateur de structures de projets professionnel, open source, pensé pour tous les devs : du·de la junior qui veut apprendre vite, à l’architecte qui veut aller encore plus vite, jusqu’au·à la devops qui veut tout automatiser.

- **Stack moderne** : Python 3.10+, FastAPI, SQLModel, Vue.js 3, SQLite
- **Interface CLI et web** (FastAPI + Vue.js, thèmes CSS inclus)
- **Brace expansion** : crée des arborescences complexes en une commande
- **Templates** : FastAPI, Vue, Docker combos, et plus
- **Preview Docker réelle** : génère, affiche l’arbre, montre les ports utilisés
- **Logs, automation, scripts rebuild, rotation, sécurité**
- **Philosophie** : “Cherish your git flow or perish!”

## Installation

```
pip install mkdf
```

## Utilisation rapide

### 1. Créer un projet FastAPI en une commande

```
mkdf create my-api fastapi
```

### 2. Générer une structure personnalisée (mode god -1)

```
mkdf my-app/{src/{api,models,services},docs/{README.md,INSTALL.md},tests/test_api.py,.env}
```

Résultat :

```
my-app/
  src/
    api/
    models/
    services/
  docs/
    README.md
    INSTALL.md
  tests/
    test_api.py
  .env
```

### 3. Docker combo avec preview réelle

```
mkdf create my-stack docker fastapi vue redis traefik --backend-port 8080 --frontend-port 3000
```

## Documentation progressive

- **Niveau 1 (débutant)** : Crée un projet à partir d’un template
- **Niveau 2 (survivalist)** : Utilise l’expansion d’accolades pour générer fichiers + dossiers
- **Niveau 3 (god mode -1)** : Compose des architectures complexes, combos Docker, ports custom

Tout est documenté dans le dossier docs/ et via mkdf --help.

## Fun fact : “SURVIVED rm -rf *”

Oui, ce projet a survécu DEUX fois à un rm -rf * accidentel.  
Chaque ligne de code, chaque test, chaque commit est une preuve de résilience et de foi dans le git flow.  
Moralité : **Cherish your git flow or perish!**

## Contribuer

- Fork, clone, propose tes idées, corrige mes bugs, ajoute tes templates, tes thèmes CSS, tes workflows.
- Rejoins la communauté (Discord/Matrix/Forum à venir).
- Respect, bienveillance et humour exigés.

## Licence

MIT – Open source, pour tous·tes.

Si tu veux des sections plus détaillées (architecture, contribution, badges supplémentaires, etc.), dis-le-moi !  
Ce squelette est prêt à être collé tel quel et enrichi plus tard.

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/22048764/bddf1f20-7e4e-4d95-b249-841b27e5497e/README.md