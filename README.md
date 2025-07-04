# MKDF – Make Directories and Files

![Version](https://img.shields.io/badge/python-3.10-4BAPI)
![Poetry](https://img.shields.io/badge/poetry-managed-4BAPI)
![FastAPI](https://img.shields.io/badge/fastapi-async-green?.js)
![Vue3](https://img.shields.io/badge/vue.js-3.x-brightgreen)
![SQLite](https://img.shields.io/badge/sqlite-embedded-lightgreyPL)
![GNU AGPL](https://img.shields.io/badge/license-AGPL)
![Cherish your Git flow or perish](https://img.shields.io/badge/Cherish%20your%20gitflow-%20or%20perish%20-red)
![Survived rm -rf *](https://img.shields.io/badge/SURVIVED---rm--rf--*-red)

## What is MKDF?

MKDF is a professional, open source project structure generator for all developers: from juniors who want to learn fast or discover new frameworks, architects who want to go even faster, to devops who want everything automated.

- Modern package stack: Python 3.10+, Poetry, automated rebuild package script
- CLI: interactive mode built with Typer and Click
- Web interface: FastAPI (SQLModel + Pydantic) + Vue.js 3 + SQLite
- Command line usage:
  - No arguments: launch CLI interactive mode, with a clear terminal.
  - Path with brace expansion: create directories and files simultaneously (mkdir + touch)
  - Create command: guided mode or one-liner for template names or docker templates
- Docker combos: multi-service docker combos ready to code, with port and docker subnet scanning to avoid conflicts

Philosophy of the project: "Cherish your git flow or perish!"

## Installation

For now, MKDF is not published on PyPI. You can install it locally using editable mode or use the rebuild script:

```bash
# clone this repo
git clone https://github.com/Noziop/mkdf-py.git ~/mkdf && cd ~/mkdf

# install the package
pip install -e .  # for now, will be pushed on PyPI soon

# or

./rebuild_mkdf.sh  # automated (re)build and install script : stop the webserver if active first, (re)build package, ask if webserver has to be restart
```

## Quick Start

### 0. How to use :

```bash
» mkdf --help

 Usage: mkdf [OPTIONS] COMMAND [ARGS]...

 MKDF - Professional project structure creator

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --interactive  -i        Launch interactive mode                                                                     │
│ --help                   Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create         Create a new project from template or Docker combo.                                                   │
│ web                                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### 1. CLI

```bash

__/\\\\____________/\\\\__/\\\________/\\\__/\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\_
 _\/\\\\\\________/\\\\\\_\/\\\_____/\\\//__\/\\\////////\\\__\/\\\///////////__
  _\/\\\//\\\____/\\\//\\\_\/\\\__/\\\//_____\/\\\______\//\\\_\/\\\_____________
   _\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\//\\\_____\/\\\_______\/\\\_\/\\\\\\\\\\\_____
    _\/\\\__\///\\\/___\/\\\_\/\\\//_\//\\\____\/\\\_______\/\\\_\/\\\///////______
     _\/\\\____\///_____\/\\\_\/\\\____\//\\\___\/\\\_______\/\\\_\/\\\_____________
      _\/\\\_____________\/\\\_\/\\\_____\//\\\__\/\\\_______/\\\__\/\\\_____________
       _\/\\\_____________\/\\\_\/\\\______\//\\\_\/\\\\\\\\\\\\/___\/\\\_____________
        _\///______________\///__\///________\///__\////////////_____\///______________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
️‍ Make Directories and Files - Professional Project Creator - By github.com/Noziop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                 Available Actions
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Option ┃ Description                            ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1      │  Create from pattern (brace expansion) │
│ 2      │  Create from template                  │
│ 3      │  Create Docker combo                   │
│ 4      │  Configure settings                    │
│ 0      │  Exit                                  │
└────────┴────────────────────────────────────────┘
Your choice:
```

### 2. Create a FastAPI project in one command

```bash
» mkdf create my-f-api fastapi                                                                                           8s 233s 89s 8s
2025-07-01 08:38:21,628 - INFO - Found available subnet: 172.22.0.0/16
2025-07-01 08:38:21,628 - INFO - Found free port: 8001
2025-07-01 08:38:21,629 - INFO - Found free port: 3000
2025-07-01 08:38:21,629 - INFO - Found free port: 6379
2025-07-01 08:38:21,629 - INFO - Found free port: 9090
2025-07-01 08:38:21,629 - INFO - Found free port: 3001
2025-07-01 08:38:21,629 - INFO - Found free port: 8082
2025-07-01 08:38:21,629 - INFO - Found free port: 8090
2025-07-01 08:38:21,630 - INFO - Found free port: 8085
╭─────────────────────────────────────────────────── ✨ Project Created Successfully ───────────────────────────────────────────────────╮
│  You're all set! Better get yourself coding this brilliant idea of yours!                                                             │
│                                                                                                                                       │
│  Project 'my-f-api' created successfully!                                                                                             │
│  Location: ./my-f-api                                                                                                                 │
│                                                                                                                                       │
│ Next steps:                                                                                                                           │
│   cd ./my-f-api                                                                                                                       │
│   pip install -r requirements.txt                                                                                                     │
│   python main.py                                                                                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```



### 3. Generate a custom structure, dir and files (oneliner)

```bash
» mkdf my-app/{src/{api,models,services},docs/{README.md,INSTALL.md},tests/test_api.py,.env}
╭────────────────────────────────────────── ✨ Project Created Successfully ───────────────────────────────────────────╮
│  You're all set! Better get yourself coding this brilliant idea of yours!                                            │
│                                                                                                                      │
│  Project 'file structure' created successfully!                                                                      │
│  Location: /home/noziop/projects/test_mkdf/my-app                                                                    │
│                                                                                                                      │
│ Next steps:                                                                                                          │
│   cd /home/noziop/projects/test_mkdf/my-app                                                                          │
│   Happy coding! 🚀                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### 34. Docker combo Creation 

```bash
» mkdf create my-stack docker fastapi vue redis traefik --backend-port 8080 --frontend-port 3000                         8s 233s 89s 8s
2025-07-01 08:34:32,500 - INFO - Found available subnet: 172.22.0.0/16
2025-07-01 08:34:32,501 - INFO - Found free port: 6379
2025-07-01 08:34:32,501 - INFO - Found free port: 9090
2025-07-01 08:34:32,501 - INFO - Found free port: 3001
2025-07-01 08:34:32,501 - INFO - Found free port: 8082
2025-07-01 08:34:32,501 - INFO - Found free port: 8090
2025-07-01 08:34:32,501 - INFO - Found free port: 8085
╭─────────────────────────────────────────────────── ✨ Project Created Successfully ───────────────────────────────────────────────────╮
│  You're all set! Better get yourself coding this brilliant idea of yours!                                                             │
│                                                                                                                                       │
│  Project 'my-stack' created successfully!                                                                                             │
│  Location: ./my-stack                                                                                                                 │
│                                                                                                                                       │
│ Next steps:                                                                                                                           │
│   cd ./my-stack                                                                                                                       │
│   Start coding!                                                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
~/projects/test_mkdf
» tree -h my-stack                                                                                                       8s 233s 89s 8s
[4.0K]  my-stack
├── [4.0K]  backend
│   ├── [ 394]  Dockerfile
│   ├── [4.0K]  app
│   │   ├── [   0]  __init__.py
│   │   ├── [4.0K]  api
│   │   │   ├── [   0]  __init__.py
│   │   │   └── [4.0K]  v1
│   │   │       ├── [   0]  __init__.py
│   │   │       ├── [4.0K]  endpoints
│   │   │       │   ├── [   0]  __init__.py
│   │   │       │   ├── [ 129]  health.py
│   │   │       │   └── [ 151]  users.py
│   │   │       └── [ 252]  router.py
│   │   ├── [4.0K]  core
│   │   │   ├── [   0]  __init__.py
│   │   │   └── [ 449]  config.py
│   │   ├── [ 587]  main.py
│   │   └── [4.0K]  models
│   │       ├── [   0]  __init__.py
│   │       └── [  96]  user.py
│   ├── [ 168]  requirements.txt
│   └── [4.0K]  tests
│       ├── [   0]  __init__.py
│       └── [ 416]  test_main.py
├── [2.0K]  docker-compose.yml
├── [4.0K]  frontend
│   ├── [ 151]  Dockerfile
│   ├── [ 291]  index.html
│   ├── [ 290]  package.json
│   ├── [4.0K]  src
│   │   ├── [ 345]  App.vue
│   │   └── [  92]  main.js
│   └── [ 179]  vite.config.js
└── [4.0K]  traefik
    └── [ 207]  traefik.yml

11 directories, 24 files
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
