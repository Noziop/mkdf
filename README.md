# MKDF – Make Directories and Files

![PyPI](https://img.shields.io/pypi/v/mkdf)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![Poetry](https://img.shields.io/badge/poetry-managed-blue)
![FastAPI](https://img.shields.io/badge/fastapi-async-green)
![SQLite](https://img.shields.io/badge/sqlite-embedded-lightgrey)
![AGPL](https://img.shields.io/badge/license-AGPL-blue)
![Release](https://img.shields.io/github/v/release/Noziop/mkdf?include_prereleases)
![Issues](https://img.shields.io/github/issues/Noziop/mkdf)
![Cherish your git flow or perish](https://img.shields.io/badge/Cherish%20your%20gitflow-or%20perish-red)
![Survived rm -rf *](https://img.shields.io/badge/SURVIVED-rm%20--rf%20*-red)

---

> **One command to create them all,  
> one command to find all ports & subnet,  
> and in the docker-compose bind them.**

---

## Why mkdf?

**You’re tired of boilerplate.**  
So was I.  
MKDF exists because we’re done wasting life on project scaffolding.  
Folders, files, docker combos: all automated.

_TL;DR: Type, hit enter, and mkdf does in milliseconds what took you hours. No bs, no fluff, no time to waste._

---

### New here? Start fast

```
mkdf --help
mkdf
mkdf create
```
And follow the prompts.

---

### Features (yes, already works)

- **CLI-first:** Type, hit enter, done.
- **Docker combos:** Auto port/subnet, compose-ready.
- **Templates:** React, Vue, FastAPI, Flask, Express, Laravel (+ soon).
- **Brace expansion:**  
  ```
  mkdf {api,utils}/test_{a,b}.py
  tree my-app
  ```
  (forests, not trees)

- **"God mode":**  
  ```
  mkdf create my-app fastapi vue redis traefik --backend-port 8080 --frontend-port 3000
  ```

---

## ⚡️ Status (v0.1.1 alpha)

- **Stable:** CLI, templates, docker combos, brace expansion.
- **WIP:** .env, backend, web UI (FastAPI+Vue).
- **Next:** Smart DB config, plugin system, cloud, PRs welcome.

---

## 🚀 Install

```
pip install mkdf
```

---

## 🛠 Usage

```
mkdf create my-f-api fastapi
mkdf my-app/{src/{api,models,services},docs/{README.md,INSTALL.md},tests/test_api.py,.env}
mkdf create my-stack docker fastapi vue redis traefik --backend-port 8080 --frontend-port 3000
tree -h my-stack
```

---

## Contribution & Feedback

- Bugs or 🚀 ideas? [Open an issue](https://github.com/Noziop/mkdf/issues).
- Use. Break. Contribute. PR. Fork. Yell.
- This is a tool *from a dev for devs*.  
  Feedback welcome (I’m done with solo rants).

---

## Docs

**WIP** — I’m rewriting all docs to reflect latest features.
*You want to help? Open a PR or hit me by issues!*

---

## License

[GNU AGPL v3.0](LICENSE) — Free as in freedom, not as in SaaS-taking.  
Commercial/SaaS use? [license@buildme.it](mailto:license@buildme.it)

---

> **Get shit done. Fast. Survive your next rm -rf.  
> mkdf — built by the person who needed it most.**
