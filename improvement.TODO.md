# TODO - Points à corriger ou améliorer (tests CLI mkdf)

- [x] Génération du .env : la variable DATABASE_URL ne doit apparaître que si une base de données est explicitement demandée lors de la création d'un projet (ex : mkdf create test-tpl fastapi --force ne devrait pas générer DATABASE_URL)

## Proposition d'amélioration pour les templates backend

**Contexte :** Les frameworks backend ont généralement besoin d'une DB pour être fonctionnels et permettre un prototypage rapide.

### Flags proposés pour tous les backends

```bash
# Cas 1 : DB explicite (priorité absolue)
mkdf create test docker fastapi postgresql
→ Utilise la config PostgreSQL

# Cas 2 : Mode prototype 
mkdf create test fastapi --proto  
→ SQLite en mémoire (rapide, temporaire)

# Cas 3 : Pas de DB (APIs stateless)
mkdf create test fastapi --no-db
→ Aucune variable DATABASE_* 

# Cas 4 : Par défaut (développement normal)
mkdf create test fastapi
→ SQLite fichier local (persistant)
```

### Harmonisation par framework (spécificités techniques détaillées)

**Architecture générale :** Créer un `BackendDBConfigFactory` qui gère les spécificités de chaque framework :

| Framework | Par défaut | --proto | --no-db | Config Type | Spécificités réelles |
|-----------|------------|---------|---------|-------------|---------------------|
| **FastAPI** | `DATABASE_URL=sqlite:///./app.db` | `DATABASE_URL=sqlite:///:memory:` | ❌ | .env | SQLAlchemy/SQLModel, async support |
| **Flask** | `DATABASE_URL=sqlite:///./app.db` | `DATABASE_URL=sqlite:///:memory:` | ❌ | .env | Flask-SQLAlchemy, `app.config['SQLALCHEMY_DATABASE_URI']` |
| **Django** | `'NAME': './db.sqlite3'` | `'NAME': ':memory:'` | ❌ | settings.py | DATABASES dict, ORM intégré |
| **Express** | `DATABASE_URL=sqlite://./app.db` | `DATABASE_URL=sqlite://:memory:` | ❌ | .env | Sequelize/Prisma/TypeORM, Node.js |
| **Laravel** | `DB_CONNECTION=sqlite`<br>`DB_DATABASE=./database.sqlite` | `DB_CONNECTION=sqlite`<br>`DB_DATABASE=:memory:` | ❌ | .env | Eloquent ORM, artisan migrations |
| **GoFiber** | `DATABASE_URL=sqlite://./app.db` | `DATABASE_URL=sqlite://:memory:` | ❌ | .env | GORM, Go structs pour modèles |

### Détails d'implémentation par framework

#### FastAPI (Python)
```python
# .env
DATABASE_URL=sqlite:///./app.db
# OU pour --proto
DATABASE_URL=sqlite:///:memory:

# Packages requis
# requirements.txt: sqlalchemy, sqlmodel (ou alembic pour migrations)
```

#### Flask (Python)  
```python
# .env
DATABASE_URL=sqlite:///./app.db
# app.py utilise: app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Packages: flask-sqlalchemy, flask-migrate
```

#### Django (Python)
```python
# settings.py - DATABASES dict (pas .env pour la config principale)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Fichier
        # OU pour --proto: 'NAME': ':memory:'
    }
}
# Migrations: python manage.py migrate
```

#### Express (Node.js)
```javascript
// .env  
DATABASE_URL=sqlite://./app.db
// Package.json: sqlite3, sequelize (ou prisma)
// sequelize config utilise process.env.DATABASE_URL
```

#### Laravel (PHP)
```php
// .env - Variables multiples (format Laravel)
DB_CONNECTION=sqlite
DB_DATABASE=./database/database.sqlite
// OU pour --proto: DB_DATABASE=:memory:
// Migrations: php artisan migrate
```

#### GoFiber (Go)
```go
// .env
DATABASE_URL=sqlite://./app.db
// go.mod: gorm.io/driver/sqlite, gorm.io/gorm
// GORM utilise la DATABASE_URL directement
```

### Implémentation proposée

1. **Nouveau factory** : `src/mkdf/templates/factories/backend_db_factory.py`
2. **Interface commune** : `generate_db_config(framework, mode)` 
3. **Modes** : `'default'`, `'proto'`, `'none'`
4. **Gestion spécifique** : Chaque framework a sa logique (variables, format, fichiers)

### 🐍 Spécifique Python : Gestion des dépendances

**Problématique :** Poetry vs pip pour les backends Python (FastAPI, Flask, Django)

**Flags proposés :**
```bash
# Par défaut = Poetry (pour les devs fainéants mais intelligents 😄)
mkdf create my-api fastapi
→ Génère pyproject.toml + poetry.lock (Poetry par défaut)

# Poetry explicite (même résultat que défaut)
mkdf create my-api fastapi --poetry
→ Génère pyproject.toml + poetry.lock

# Pip pour les nostalgiques  
mkdf create my-api fastapi --pip
→ Génère requirements.txt
```

**Avantages Poetry :**
- ✅ **Gestion des versions** : résolution automatique des conflits
- ✅ **Environnement virtuel** : création et gestion automatique
- ✅ **Fichier lock** : builds reproductibles 
- ✅ **Méta-données** : projet + dépendances dans un seul fichier
- ✅ **Professionnel** : standard moderne Python

**Configuration par framework Python :**

| Framework | --poetry | --pip | Packages spécifiques |
|-----------|----------|-------|---------------------|
| **FastAPI** | `pyproject.toml` + SQLAlchemy/SQLModel | `requirements.txt` | uvicorn, fastapi |
| **Flask** | `pyproject.toml` + Flask-SQLAlchemy | `requirements.txt` | flask, flask-sqlalchemy |
| **Django** | `pyproject.toml` + Django ORM | `requirements.txt` | django, django-extensions |

**Implémentation :**
- **Template différentiel** : même structure de fichiers, différent gestionnaire de deps
- **Scripts inclus** : `poetry install` vs `pip install -r requirements.txt`
- **Commandes de dev** : `poetry run` vs activation venv manuelle

**Avantages :**
- ✅ Cohérence : même logique pour tous les backends
- ✅ Flexibilité : chaque framework garde ses spécificités  
- ✅ Maintenabilité : code centralisé et réutilisable
- ✅ Extensibilité : facile d'ajouter de nouveaux frameworks
- ✅ **Modernité** : Poetry par défaut pour Python

### 🏆 MKDF = Champion du scaffolding moderne !

**Philosophie "lazy but smart" :**
- ✅ **Zéro configuration** : Poetry + SQLite par défaut
- ✅ **Conventions over configuration** : choix sensés par défaut
- ✅ **Productivité ultime** : API prête en millisecondes !

**Performance de scaffolding :**
```bash
mkdf create my-awesome-api fastapi  # <- 30 millisecondes ⚡
cd my-awesome-api                   # <- 10 millisecondes  
poetry install                      # <- 2-3 secondes max
poetry run uvicorn main:app --reload # <- 500ms pour démarrer
```

**🚀 Total : API fonctionnelle en moins de 5 secondes !**
*Ça c'est du scaffolding de champion !* ⚡💪

(La liste sera complétée au fur et à mesure des tests CLI et des vérifications de conformité)
