import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, TypedDict

class PortConfig(TypedDict, total=False):
    backend: int
    frontend: int
    database: int
    redis: int
    subnet: str
    prometheus: int
    grafana: int
    traefik: int
    traefik_dashboard: int

ProjectStructure = Dict[str, Union[str, Dict[str, Any]]]

DOCKER_COMPONENT_CATEGORIES = {
    "Backend": ["fastapi", "flask", "express", "gofiber"],
    "Frontend": ["vue", "react", "svelte", "angular", "nextjs", "nuxtjs"],
    "Fullstack": ["laravel", "django", "symfony"],
    "Database": ["postgresql", "mysql", "mongodb"],
    "Cache/Queue": ["redis", "celery", "rabbitmq"],
    "Proxy": ["nginx", "traefik"],
    "Monitoring": ["monitoring", "prometheus", "grafana", "loki"]
}

def detect_monitoring_conflicts(components: List[str]) -> None:
    """Detect conflicts between monitoring meta-component and individual services"""
    monitoring_services = {'prometheus', 'grafana', 'loki'}

    if 'monitoring' in components:
        conflicts = [comp for comp in components if comp in monitoring_services]
        if conflicts:
            raise ValueError(
                f"Cannot use 'monitoring' with individual monitoring services: {', '.join(conflicts)}. "
                "Choose one option:\n"
                "1. Use 'monitoring' for complete stack (prometheus + grafana + loki)\n"
                "2. Use individual services: " + ', '.join(conflicts)
            )

DOCKER_MODULES = {
    # Backend
    'fastapi': {
        'path': 'backend',
        'files': {
            'app/main.py': '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
''',
            'app/__init__.py': '',
            'app/api/__init__.py': '',
            'app/api/v1/__init__.py': '',
            'app/api/v1/router.py': '''from fastapi import APIRouter
from app.api.v1.endpoints import users, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
''',
            'app/api/v1/endpoints/__init__.py': '',
            'app/api/v1/endpoints/users.py': '''from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
''',
            'app/api/v1/endpoints/health.py': '''from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy"}
''',
            'app/core/__init__.py': '',
            'app/core/config.py': '''from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    DATABASE_URL: str = "postgresql://user:password@db:5432/dbname"
    SECRET_KEY: str = "your-secret-key-here"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
''',
            'app/models/__init__.py': '',
            'app/models/user.py': '''from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
''',
            'tests/__init__.py': '',
            'tests/test_main.py': '''from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI App"}

def test_health_check():
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
''',
            'requirements.txt': '''fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-decouple==3.8
pydantic-settings==2.0.3
''',
            '.env.backend': '''DATABASE_URL=postgresql://user:password@db:5432/dbname
SECRET_KEY=your-secret-key-here
DEBUG=true
'''
        },
        'dockerfile_content': '''FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
''',
        'compose_service': {
            'build': {
                'context': './backend',
                'dockerfile': 'Dockerfile'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-backend',
            'ports': ['8000'],
            'environment': [
                'DATABASE_URL=postgresql://${POSTGRES_USER:-user}:${POSTGRES_PASSWORD:-password}@db:5432/${POSTGRES_DB:-dbname}',
                'SECRET_KEY=${SECRET_KEY}',
                'DEBUG=${DEBUG}'
            ],
            'volumes': ['./backend:/app'],
            'depends_on': ['postgresql'],
            'networks': ['app-network']
        }
    },
    'flask': {'path': 'backend', 'files': {'app.py': ''}, 'dockerfile_content': '', 'compose_service': {}},
    'express': {'path': 'backend', 'files': {'app.js': ''}, 'dockerfile_content': '', 'compose_service': {}},
    'gofiber': {'path': 'backend', 'files': {'main.go': ''}, 'dockerfile_content': '', 'compose_service': {}},
    # Frontend
    'vue': {
        'path': 'frontend',
        'files': {
            'package.json': '''{
  "name": "vue-app",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.4"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.4.0",
    "vite": "^4.4.5"
  }
}''',
            'vite.config.js': '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3000
  }
})
''',
            'index.html': '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vue App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>''',
            'src/main.js': '''import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
''',
            'src/App.vue': '''<template>
  <div id="app">
    <h1>Hello Vue!</h1>
    <p>Your Vue app is running successfully.</p>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  text-align: center;
  padding: 20px;
}
</style>
'''
        },
        'dockerfile_content': '''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
''',
        'compose_service': {
            'build': {
                'context': './frontend',
                'dockerfile': 'Dockerfile'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-frontend',
            'ports': ['3000'],
            'environment': ['VITE_API_URL=http://localhost/api'],
            'volumes': ['./frontend:/app'],
            'networks': ['app-network']
        }
    },
    'react': {'path': 'frontend', 'files': {'App.js': ''}, 'dockerfile_content': '', 'compose_service': {}},
    'svelte': {'path': 'frontend', 'files': {'App.svelte': ''}, 'dockerfile_content': '', 'compose_service': {}},
    'angular': {'path': 'frontend', 'files': {'app.component.ts': ''}, 'dockerfile_content': '', 'compose_service': {}},
    'nextjs': {'path': 'frontend', 'files': {'pages/index.js': ''}, 'dockerfile_content': '', 'compose_service': {}},
    'nuxtjs': {'path': 'frontend', 'files': {'pages/index.vue': ''}, 'dockerfile_content': '', 'compose_service': {}},
    # Fullstack
    'laravel': {'path': 'backend', 'files': {}, 'dockerfile_content': '', 'compose_service': {}},
    'django': {'path': 'backend', 'files': {}, 'dockerfile_content': '', 'compose_service': {}},
    'symfony': {'path': 'backend', 'files': {}, 'dockerfile_content': '', 'compose_service': {}},
    # Database
    'postgresql': {
        'path': 'database',
        'compose_service': {
            'image': 'postgres:15-alpine',
            'container_name': '${PROJECT_NAME:-fullstack}-db',
            'environment': [
                'POSTGRES_USER=${POSTGRES_USER:-user}',
                'POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-password}',
                'POSTGRES_DB=${POSTGRES_DB:-dbname}'
            ],
            'ports': ['5432'],
            'volumes': ['postgres_data:/var/lib/postgresql/data'],
            'networks': ['app-network']
        }
    },
    'mysql': {'path': 'database', 'compose_service': {}},
    'mongodb': {'path': 'database', 'compose_service': {}},
    # Cache/Queue
    'redis': {
        'path': 'cache',
        'compose_service': {
            'image': 'redis:7-alpine',
            'container_name': '${PROJECT_NAME:-fullstack}-redis',
            'ports': ['6379'],
            'volumes': ['redis_data:/data'],
            'networks': ['app-network']
        }
    },
    'celery': {'path': 'cache', 'compose_service': {}},
    'rabbitmq': {'path': 'cache', 'compose_service': {}},
    # Proxy
    'nginx': {'path': 'proxy', 'compose_service': {}},
    'traefik': {
        'path': 'traefik',
        'files': {
            'traefik.yml': '''api:
  dashboard: true
  insecure: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
'''
        },
        'compose_service': {
            'image': 'traefik:v3.0',
            'container_name': '${PROJECT_NAME:-fullstack}-traefik',
            'command': ['--configFile=/traefik.yml'],
            'ports': ['80:80', '443:443', '8080:8080'],
            'volumes': [
                '/var/run/docker.sock:/var/run/docker.sock:ro',
                './traefik/traefik.yml:/traefik.yml:ro'
            ],
            'networks': ['app-network']
        }
    },
    # Monitoring
    'monitoring': {'path': 'monitoring', 'compose_service': {}},
    'prometheus': {'path': 'monitoring', 'compose_service': {}},
    'grafana': {'path': 'monitoring', 'compose_service': {}},
    'loki': {'path': 'monitoring', 'compose_service': {}}
}

def get_docker_template(
    components: Optional[List[str]] = None,
    project_name: Optional[str] = None,
    port_config: Optional[PortConfig] = None
) -> ProjectStructure:
    """Generate Docker template with configurable ports and subnet."""
    
    if components is None:
        components = []
    if project_name is None:
        project_name = "fullstack-app"
    if port_config is None:
        port_config = {
            'backend': 8000,
            'frontend': 3000,
            'database': 5432,
            'redis': 6379,
            'subnet': '172.18.0.0/16',
            'prometheus': 9090,
            'grafana': 3001,
            'traefik': 80,
            'traefik_dashboard': 8080,
        }

    # Detect monitoring conflicts
    detect_monitoring_conflicts(components)
    
    project_structure = {}
    docker_compose_services = {}
    docker_compose_volumes = {}
    network_name = f"{project_name}_app-network"
    
    docker_compose_networks = {
        network_name: {
            'driver': 'bridge',
            'ipam': {
                'config': [{
                    'subnet': port_config.get('subnet', '172.18.0.0/16')
                }]
            }
        }
    }

    # Root level files
    project_structure['.env'] = f'''PROJECT_NAME={project_name}
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=dbname
SECRET_KEY=your-super-secret-key-here
DEBUG=true
'''

    # Handle monitoring meta-component
    if 'monitoring' in components:
        prometheus_port = port_config.get('prometheus', 9090)
        grafana_port = port_config.get('grafana', 3001)

        docker_compose_services['prometheus'] = {
            'image': 'prom/prometheus',
            'container_name': f'{project_name}-prometheus',
            'ports': [f"{prometheus_port}:9090"],
            'volumes': ['./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml'],
            'networks': [network_name]
        }

        docker_compose_services['grafana'] = {
            'image': 'grafana/grafana',
            'container_name': f'{project_name}-grafana',
            'ports': [f"{grafana_port}:3000"],
            'environment': ['GF_SECURITY_ADMIN_PASSWORD=admin'],
            'depends_on': ['prometheus'],
            'networks': [network_name]
        }

        project_structure['monitoring/prometheus.yml'] = '''global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
'''

        # Remove monitoring from further processing
        components = [c for c in components if c != 'monitoring']

    # Process each component
    for component in components:
        module_config = DOCKER_MODULES.get(component)
        if not module_config:
            raise ValueError(f"Unknown Docker component: {component}")

        component_path = module_config.get('path', component)

        # Add files to project structure
        if 'files' in module_config:
            for file_path, content in module_config['files'].items():
                full_path = os.path.join(component_path, file_path)
                parts = Path(full_path).parts
                current_dict = project_structure
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:
                        current_dict[part] = content
                    else:
                        if part not in current_dict or not isinstance(current_dict[part], dict):
                            current_dict[part] = {}
                        current_dict = current_dict[part]

        # Add Dockerfile content
        if 'dockerfile_content' in module_config:
            dockerfile_path = os.path.join(component_path, 'Dockerfile')
            parts = Path(dockerfile_path).parts
            current_dict = project_structure
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    current_dict[part] = module_config['dockerfile_content']
                else:
                    if part not in current_dict or not isinstance(current_dict[part], dict):
                        current_dict[part] = {}
                    current_dict = current_dict[part]

        # Add compose services
        if 'compose_service' in module_config:
            service_config = module_config['compose_service'].copy()

            # Apply port configuration
            if component in ['fastapi']:
                backend_port = port_config.get('backend', 8000)
                service_config['ports'] = [f"{backend_port}:8000"]
            elif component in ['vue']:
                frontend_port = port_config.get('frontend', 3000)
                service_config['ports'] = [f"{frontend_port}:3000"]
            elif component == 'postgresql':
                db_port = port_config.get('database', 5432)
                service_config['ports'] = [f"{db_port}:5432"]
            elif component == 'redis':
                redis_port = port_config.get('redis', 6379)
                service_config['ports'] = [f"{redis_port}:6379"]
            elif component == 'traefik':
                traefik_port = port_config.get('traefik', 80)
                traefik_dashboard = port_config.get('traefik_dashboard', 8080)
                service_config['ports'] = [
                    f"{traefik_port}:80",
                    "443:443",
                    f"{traefik_dashboard}:8080"
                ]

            # Update network
            if 'networks' in service_config:
                service_config['networks'] = [network_name]

            docker_compose_services[component] = service_config

            # Extract volumes
            if 'volumes' in service_config:
                for volume_mapping in service_config['volumes']:
                    if ':' in volume_mapping:
                        volume_name = volume_mapping.split(':')[0]
                        if not volume_name.startswith('.') and not volume_name.startswith('/'):
                            docker_compose_volumes[volume_name] = None

    # Create data directories
    data_dirs = {}
    for component in components:
        if component == 'postgresql':
            data_dirs['data/postgresql'] = {}
            data_dirs['data/postgresql/.gitkeep'] = ''
        elif component == 'redis':
            data_dirs['data/redis'] = {}
            data_dirs['data/redis/.gitkeep'] = ''

    if 'monitoring' in (components + ['monitoring'] if 'monitoring' in components else []):
        data_dirs['data/prometheus'] = {}
        data_dirs['data/grafana'] = {}
        data_dirs['data/prometheus/.gitkeep'] = ''
        data_dirs['data/grafana/.gitkeep'] = ''

    # Add data directories to project structure
    for data_path, content in data_dirs.items():
        parts = Path(data_path).parts
        current_dict = project_structure
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current_dict[part] = content
            else:
                if part not in current_dict:
                    current_dict[part] = {}
                current_dict = current_dict[part]

    # Construct docker-compose.yml
    compose_content = ["version: '3.8'", "", "services:"]
    for service_name, service_config in docker_compose_services.items():
        compose_content.append(f"  {service_name}:")
        for key, value in service_config.items():
            if key == 'build' and isinstance(value, dict):
                compose_content.append("    build:")
                compose_content.append(f"      context: {value['context']}")
                compose_content.append(f"      dockerfile: {value['dockerfile']}")
            elif isinstance(value, list):
                compose_content.append(f"    {key}:")
                for item in value:
                    compose_content.append(f"      - {item}")
            elif isinstance(value, dict):
                compose_content.append(f"    {key}:")
                for sub_key, sub_value in value.items():
                    compose_content.append(f"      {sub_key}: {sub_value}")
            else:
                compose_content.append(f"    {key}: {value}")
        compose_content.append("")

    if docker_compose_volumes:
        compose_content.append("volumes:")
        for volume_name in docker_compose_volumes.keys():
            compose_content.append(f"  {volume_name}:")
        compose_content.append("")

    compose_content.append("networks:")
    for network_name_key, network_config in docker_compose_networks.items():
        compose_content.append(f"  {network_name_key}:")
        for key, value in network_config.items():
            compose_content.append(f"    {key}: {value}")

    project_structure['docker-compose.yml'] = "\n".join(compose_content)

    return project_structure