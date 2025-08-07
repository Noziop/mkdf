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

> **One command to create them all, one command to find all ports & subnet, and in the docker-compose bind them.**

---
## Why mkdf?
### A word from the tool that made this tool

Bored of boilerplate, mkdir, touch, copy/paste, failed docker-compose, manual everything?  
So am I.  nah, sorry, SO WAS I.
MKDF exists because some of us are just done losing time on scaffolding.  
Folders, files, docker combos

Being lazy but smart, I built this tool to automate the boring stuff.  
No more manual setup, no more boilerplate hell.  
Just type, hit enter, and let mkdf do in milliseconds what you used to do in hours.  
srsly. no bs, no fluff, just code that brilliant idea of yours : we ain't have time to waste.  

---



### Not so sure whatcha doing here ?

No worries, we got your back.

>hint : type `mkdf --help` or `mkdf --create --help` first.

if you want to be guided: just type `mkdf` or `mkdf create` and follow the prompts.

### Feeling quite confident?

- **CLI-first.** Type, hit enter, done.  
- **Docker combos:** automatic port/subnet, compose-ready.
- **Templates:** React, Vue, FastAPI, Flask, Express, Laravel (+ more soon).

### got skills?

- **Brace expansion:**  

```bash
mkdf {api,utils}/test_{a,b}.py` # forests, not trees.
tree my-app
 my-app/
 ├── src/
 │   ├── api/
 │   └── utils/
 └── tests/
   ├── test_a.py
   └── test_b.py
```

### God mode?
1- Create a new project with all the bells and whistles:
```bash
mkdf create my-app fastapi vue redis traefik --backend-port 8080 --frontend-port 3000
```
```bash
tree my-app
  my-app/
  ├── src/
  │   ├── api/
  │   ├── models/
  │   └── services/
  ├── docs/
  │   ├── README.md
  │   └── INSTALL.md
  ├── tests/
  │   └── test_api.py
  ├── .env
```

2-create a directory structure with files:
```bash
mkdf my-app/{src/{api,models,services},docs/{README.md,INSTALL.md},tests/test_api.py,.env}
```
```bash
tree my-app
  my-app/
  ├── src/
  │   ├── api/
  │   ├── models/
  │   └── services/
  ├── docs/
  │   ├── README.md
  │   └── INSTALL.md
  ├── tests/
  │   └── test_api.py
  └── .env
``` 
---

**Radical honesty:** TODO = not done;  
alpha = truly alpha.  
“Cherish your git flow or perish!” — more slogan, it’s a survival hack.  

---

## ⚡️ Status (v0.1.1 alpha)

- **Stable:** CLI, templates, docker combos, expansion.
- **WIP:** .env, backend, web UI (FastAPI+Vue).
- **Next:** Smart DB config, plugin system, cloud, PRs welcome.

---

## 🚀 Install

```
git clone https://github.com/Noziop/mkdf.git ~/mkdf && cd ~/mkdf
pip install -e .
# Or: ./rebuild_mkdf.sh
```

---

## Usage

```
mkdf create my-f-api fastapi
mkdf my-app/{src/{api,models,services},docs/{README.md,INSTALL.md},tests/test_api.py,.env}
mkdf create my-stack docker fastapi vue redis traefik --backend-port 8080 --frontend-port 3000
tree -h my-stack
```

---

## Contribution & Feedback

- Bugs or wild ideas? [Open an issue](https://github.com/Noziop/mkdf/issues).  
- Use. Break. Improve. PR. Fork. Yell.
- The tool that made this tool wants your feedback. (Because I’m done with solo rants.)


## Docs

coming soon: working on it RN (not talking about the fascist french political party).

## License

[GNU AGPL v3.0](LICENSE) — OSS for all.  
For closed source/SaaS: [license@buildme.it](mailto:license@buildme.it)

---

> **Get shit done. Fast. Survive your next rm -rf.  
> mkdf — built by the person who needed it most.**
