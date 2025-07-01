# MKDF – Make Directories and Files

[![Python](https://img.shields.io/badge/python-3.10%etry](https://img.shields.io/badge/poetry-managed-4BAPI](https://img.shields.io/badge/fastapi-async-green?.js](https://img.shields.io/badge/vue.js-3.x-brightgreen](https://img.shields.io/badge/sqlite-embedded-lightgreyPL v3](https://img.shields.io/badge/license-AGPL--vish your git flow or perish!](https://img.shields.io/badge/cherish%20your%20git%20flow%20or%20perishvived rm -rf *](https://img.shields.io/badge/SURVIVED--rm--rf--*-redish your git flow or perish!

## What is MKDF?

MKDF is a professional, open source project structure generator for all developers: from juniors who want to learn fast or discover new frameworks, to architects who want to go even faster, to devops who want everything automated.

- Modern package stack: Python 3.10+, Poetry, automated rebuild package script
- CLI: interactive mode built with Typer and Click
- Web interface: FastAPI (SQLModel + Pydantic) + Vue.js 3 + SQLite
- Command line usage:
  - No arguments: launch CLI interactive mode
  - Path with brace expansion: create directories and files simultaneously (mkdir + touch)
  - Create command: guided mode or one-liner for template names or docker templates
- Docker combos: multi-service docker combos ready to code, with port and docker subnet scanning to avoid conflicts

Philosophy of the project: "Cherish your git flow or perish!"

## Installation

For now, MKDF is not published on PyPI. You can install it locally using editable mode or use the rebuild script:

```bash
pip install -e .  # for now, will be pushed on PyPI soon

# or

./rebuild_mkdf.sh  # automated (re)build and install script : stop the webserver if active first, (re)build package, ask if webserver has to be restart
```

## Quick Start

### 1. Create a FastAPI project in one command

```bash
mkdf create my-api fastapi
```

Example output of tree -h after creation:

```bash
» tree -h projetcombo
[4.0K]  projetcombo
├── [4.0K]  backend
│   ├── [ 394]  Dockerfile
│   ├── [4.0K]  app
│   │   ├── [   0]  __init__.py
│   │   ├── [4.0K]  api
│   │   │   ├── [   0]  __init__.py
│   │   │   └── [4.0K]  v1
│   │   │       ├── [   0]  __init__.py
│   │   │       ├── [4.0K]  endpoints
│   │   │       │   ├── [   0]  __init__.py
│   │   │       │   ├── [ 129]  health.py
│   │   │       │   └── [ 151]  users.py
│   │   │       └── [ 252]  router.py
│   │   ├── [4.0K]  core
│   │   │   ├── [   0]  __init__.py
│   │   │   └── [ 449]  config.py
│   │   ├── [ 587]  main.py
│   │   └── [4.0K]  models
│   │       ├── [   0]  __init__.py
│   │       └── [  96]  user.py
│   ├── [ 168]  requirements.txt
│   └── [4.0K]  tests
│       ├── [   0]  __init__.py
│       └── [ 416]  test_main.py
├── [ 981]  docker-compose.yml
└── [4.0K]  frontend
    ├── [ 151]  Dockerfile
    ├── [ 291]  index.html
    ├── [ 290]  package.json
    ├── [4.0K]  src
    │   ├── [ 345]  App.vue
    │   └── [  92]  main.js
    └── [ 179]  vite.config.js

10 directories, 23 files
```

### 2. Generate a custom structure (god mode -1)

```bash
mkdf my-app/{src/{api,models,services},docs/{README.md,INSTALL.md},tests/test_api.py,.env}
```

### 3. Docker combo with real preview

```bash
mkdf create my-stack docker fastapi vue redis traefik --backend-port 8080 --frontend-port 3000
```

## Documentation and Organization

- Templates listing and details moved to docs/templates.md
- CLI interactive mode, simple patterns, and template usage detailed in docs/JUNIOR.md
- Web interface usage and features in docs/LAZYDEV.md
- Docker combos and advanced usage in docs/SENIOR.md
- God mode -1: advanced docker combos with port management in docs/GODMODE.md
- Fun facts and project philosophy in docs/FUN_FACTS.md
- Full contribution process in docs/CONTRIBUTING.md

Note: Logging and log rotation are not yet implemented in the app and will be addressed in future updates.

## Fun facts

- This project survived two accidental rm -rf * (and so did the dev).
- “Cherish your git flow or perish!” is not just a slogan, it’s a way of life here.
- All community suggestions are welcome, even the wildest ones.

## Contribution

- Fork, clone, propose ideas, fix bugs, add templates, CSS themes, or workflows.
- Join the community (Discord/Matrix/Forum coming soon).
- Respect, kindness, and humor required.
- See docs/CONTRIBUTING.md for the full process.

## License

GNU Affero General Public License v3 (AGPL) – Open source, for everyone.

```

N’hésite pas à adapter, compléter ou corriger ce texte.  
Prêt à être collé, badges à personnaliser selon tes besoins !