# MKDF – Make Directories and Files

![Version](https://img.shields.io/badge/python-3.10+-blue)
![Poetry](https://img.shields.io/badge/poetry-managed-blue)
![FastAPI](https://img.shields.io/badge/fastapi-async-green)
![SQLite](https://img.shields.io/badge/sqlite-embedded-lightgrey)
![GNU AGPL](https://img.shields.io/badge/license-AGPL-blue)
![GitHub release](https://img.shields.io/github/v/release/Noziop/mkdf?include_prereleases)
![GitHub issues](https://img.shields.io/github/issues/Noziop/mkdf)
![Cherish your Git flow or perish](https://img.shields.io/badge/Cherish%20your%20gitflow-%20or%20perish%20-red)
![Survived rm -rf *](https://img.shields.io/badge/SURVIVED-rm%20--rf%20*-red)

---

## What is MKDF?

> **One command to create them all, one command to find all ports and subnet, and in the docker-compose bind them.**

MKDF is a professional, open source project structure generator for all developers:  
from juniors who want to learn fast or discover new frameworks, architects who want to go even faster, to DevOps who want everything automated.

- **Modern stack**: Python 3.10+, Poetry, automated rebuild script
- **CLI**: interactive mode built with Typer and Click
- **Web interface**: FastAPI (SQLModel + Pydantic) + Vue.js 3 + SQLite (coming soon, sorry for the delay, love.)
- **Usage highlights:**
  - No arguments → launch CLI interactive mode, clear terminal
  - Path with brace expansion → create dirs/files simultaneously (mkdir + touch)
  - `create` command → guided or one-liner, for templates or docker combos
- **Docker combos:** multi-service docker combos with automatic port & subnet conflict-detection (yup! you dreamed it, we did it.)

> Project philosophy: **"Cherish your git flow or perish!"**

---

## ⚠️ Current Status (v0.1.1 Alpha)

🚧 **MKDF is in active development — with full transparency.**

**What works great:**
- ✅ **CLI Interface**: fully operational & stable
- ✅ **Project Templates**: React, Vue, FastAPI, Flask, Express, Laravel, etc.
- ✅ **Docker Combos**: multi-service with auto port/subnet
- ✅ **Brace Expansion**: power-create with `{dir1,dir2}/{file1,file2}`

**Work in progress:**
- 🔧 **.env generation**: needs refinement
- 🔧 **Backend Templates**: SQLite defaults, Poetry integration
- 🔧 **Web Interface**: under migration (FastAPI + Vue.js modernization)

**Upcoming:**
- 🎯 **Smart DB Config**: SQLite by default, `--proto` for memory DB, `--no-db` for stateless APIs
- 🎯 **Poetry First**: Modern Python dependency management
- 🎯 **Unified Backend Factory**

**Why share this early?**  
We believe in transparent development. MKDF already solves real developer pains — community feedback helps us prioritize the RIGHT improvements.

> PLEASE SHARE YOUR FEEDBACK, SUGGESTIONS, AND IMPROVEMENTS : [GitHub Issues](https://github.com/Noziop/mkdf/issues)
> PLEASE, Onboard your ideas, suggestions, and improvements. We love them all : and we need your help to make MKDF even better! Become part of the community! **lonely, i feel so lonely...**

**Recommended usage:** CLI interface for all operations. Avoid web interface until migration completes.

---

## ⚠️ Legacy Status Info

- **CLI Interface**: ✅ Fully operational
- **CMD path/template/docker-combos**: ✅ Fully operational
- **Web Interface**: 🔄 Under stack migration — temporarily non-functional

> The web server starts but project creation is currently unavailable due to ongoing migration (FastAPI + Vue.js modernization).

---

## Installation

MKDF is not published on PyPI (yet!). Install locally or use the rebuild script:

```
# Clone this repo
git clone https://github.com/Noziop/mkdf.git ~/mkdf && cd ~/mkdf

# Install the package
pip install -e .  # will be pushed on PyPI soon

# Or:
./rebuild_mkdf.sh
# Automated (re)build & install: stops webserver if active, (re)builds the package, proposes restart.
```

---

## Quick Start

### 0. How to use:

```
mkdf --help

Usage: mkdf [OPTIONS] COMMAND [ARGS]...
```

### 1. CLI Example

```
mkdf create my-f-api fastapi
# ...automatic port/subnet detection
# --> Project created, ready to code!
```

### 2. Custom structure generator (one-liner)

```
mkdf my-app/{src/{api,models,services},docs/{README.md,INSTALL.md},tests/test_api.py,.env}
# --> Structure created, just start coding!
```

### 3. Docker combo creation

```
mkdf create my-stack docker fastapi vue redis traefik --backend-port 8080 --frontend-port 3000

tree -h my-stack
# Shows the full generated project tree (backend, frontend, Dockerfiles, etc.)
```

---

## Documentation and Organization

- Templates: docs/templates.md
- CLI: docs/JUNIOR.md
- Web UI usage: docs/LAZYDEV.md
- Docker combos, advanced: docs/SENIOR.md
- Hardcore/Godmode: docs/GODMODE.md
- Fun facts/philosophy: docs/FUN_FACTS.md

> *Logging/log rotation not yet implemented. Coming soon!*

---

## Fun facts

- This project survived two accidental `rm -rf *` (and so did the dev).
- “Cherish your git flow or perish!” is not just a slogan, it’s a way of life here.
- All community suggestions are welcome, even the wildest.
- **Legend says:** mkdf = “Make Dat Fucker Create”

---

## Contributing

MKDF is in active dev — code contributions on hold (for now), but we LOVE:
- Bug reports
- Feature suggestions
- Docs improvements
- Usage feedback

Commercial partnership? Contact [license@buildme.it](mailto:license@buildme.it).

---

## License

MKDF is under [GNU Affero General Public License v3.0](LICENSE).

You’re free to use, modify, and distribute MKDF for:
- Personal/dev learning
- Student/educational projects
- Freelance/client projects (as a generator)
- Internal company use (if AGPL requirements are met)

**For closed-source or SaaS distribution (see below), a commercial license is available.**  
Contact: [license@buildme.it](mailto:license@buildme.it)

**Why AGPL?**  
We believe ALL improvements should benefit the whole community. AGPL ensures that open source wins, always.

---

> **Sometimes, the only thing that matters is to get things done. Fast.**
