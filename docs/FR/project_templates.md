# Modèles de projets MKDF

MKDF propose plusieurs modèles prédéfinis pour démarrer rapidement différents types de projets. Ce guide décrit en détail chaque modèle et sa structure.

## Projet simple

Structure minimaliste adaptée aux petits projets ou comme point de départ.

```
projet/
├── src/
├── docs/
├── tests/
└── README.md
```

Commande CLI:
```bash
mkdf -c mon-projet simple
```

## Projet multi-répertoires

Structure plus complète avec séparation des composants logiques.

```
projet/
├── src/
│   ├── lib/
│   ├── bin/
│   └── include/
├── docs/
│   ├── user/
│   └── dev/
├── tests/
├── examples/
├── README.md
└── LICENSE
```

Commande CLI:
```bash
mkdf -c mon-projet multi
```

## Projet avec Docker

Structure incluant une configuration Docker pour le développement et le déploiement.

```
projet/
├── src/
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx/
│       └── default.conf
├── scripts/
│   ├── build.sh
│   └── deploy.sh
├── config/
├── docs/
├── .dockerignore
├── README.md
└── LICENSE
```

Commande CLI:
```bash
mkdf -c mon-projet docker
```

## Projet FastAPI

Structure complète pour une application backend basée sur FastAPI.

```
projet/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── endpoints/
│   │   │       ├── users.py
│   │   │       └── items.py
│   │   ├── router/
│   │   │   ├── deps.py
│   │   │   └── router.py
│   │   └── __init__.py
│   ├── service/
│   ├── models/
│   ├── utils/
│   ├── main.py
│   └── __init__.py
├── tests/
├── config/
│   └── settings.py
├── requirements.txt
├── Dockerfile
└── README.md
```

Commande CLI:
```bash
mkdf -c mon-api fastapi
```

## Projet Vue+Vite

Configuration pour un projet frontend moderne avec Vue.js et Vite.

```
projet/
├── src/
│   ├── components/
│   ├── views/
│   ├── store/
│   ├── router/
│   ├── assets/
│   ├── App.vue
│   └── main.js
├── public/
│   └── index.html
├── package.json
├── vite.config.js
├── .eslintrc.js
├── .gitignore
└── README.md
```

Commande CLI:
```bash
mkdf -c mon-frontend vue-vite
```

## Projet Flask

Structure pour une application web Python avec Flask.

```
projet/
├── app/
│   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── routes/
│   ├── models/
│   ├── __init__.py
│   └── config.py
├── tests/
├── requirements.txt
├── wsgi.py
├── .env
└── README.md
```

Commande CLI:
```bash
mkdf -c mon-website flask
```

## Projet React

Configuration pour une application frontend React.

```
projet/
├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── context/
│   ├── utils/
│   ├── App.js
│   └── index.js
├── public/
│   └── index.html
├── package.json
├── .eslintrc.js
├── .gitignore
└── README.md
```

Commande CLI:
```bash
mkdf -c mon-app react
```

## Personnaliser les modèles

Pour adapter un modèle à vos besoins, vous pouvez :

1. Créer d'abord le projet à partir d'un modèle
2. Ajouter ensuite des fichiers ou répertoires avec la syntaxe d'expansion

Exemple :
```bash
# Créer un projet FastAPI
mkdf -c mon-api fastapi

# Ajouter des composants supplémentaires
cd mon-api
mkdf 'docs/{api/,deployment/,architecture.md}'
```

---

## Navigation

- [Retour à l'index](index.md)
- Pages connexes :
  - [Utilisation en ligne de commande](cli_usage.md)
  - [Interface Web](web_usage.md)
- [Cas d'utilisation](use_cases.md) - Voir des exemples pratiques