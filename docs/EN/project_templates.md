# MKDF Project Templates

MKDF offers several predefined templates to quickly start different types of projects. This guide describes each template and its structure in detail.

## Simple Project

Minimalist structure suitable for small projects or as a starting point.

```
project/
├── src/
├── docs/
├── tests/
└── README.md
```

CLI Command:
```bash
mkdf -c my-project simple
```

## Multi-directory Project

More complete structure with separation of logical components.

```
project/
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

CLI Command:
```bash
mkdf -c my-project multi
```

## Docker Project

Structure including Docker configuration for development and deployment.

```
project/
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

CLI Command:
```bash
mkdf -c my-project docker
```

## FastAPI Project

Complete structure for a backend application based on FastAPI.

```
project/
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

CLI Command:
```bash
mkdf -c my-api fastapi
```

## Vue+Vite Project

Configuration for a modern frontend project with Vue.js and Vite.

```
project/
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

CLI Command:
```bash
mkdf -c my-frontend vue-vite
```

## Flask Project

Structure for a Python web application with Flask.

```
project/
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

CLI Command:
```bash
mkdf -c my-website flask
```

## React Project

Configuration for a React frontend application.

```
project/
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

CLI Command:
```bash
mkdf -c my-frontend react
```

## Customizing Templates

To adapt a template to your needs, you can:

1. First create the project from a template
2. Then add additional files or directories using expansion syntax

Example:
```bash
# Create a FastAPI project
mkdf -c my-api fastapi

# Add additional components
cd my-api
mkdf 'docs/{api/,deployment/,architecture.md}'
```

---

## Navigation

- [Back to Index](index.md)
- Related pages:
  - [Command Line Usage](cli_usage.md)
  - [Web Interface](web_usage.md)
- [Use Cases](use_cases.md)