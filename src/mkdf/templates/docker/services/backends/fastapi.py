from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class FastAPIService(DockerService):
    from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class FastAPIService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        db_config = detect_database_service(components)

        environment = [
            'SECRET_KEY=${SECRET_KEY}',
            'DEBUG=${DEBUG}'
        ]
        depends_on = []

        if db_config:
            environment.append(f'DATABASE_URL={db_config["url_template"]}')
            depends_on.append(db_config['service_name'])

        config = {
            'build': {
                'context': './backend',
                'dockerfile': 'Dockerfile'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-backend',
            'ports': ['8000'],
            'environment': environment,
            'volumes': ['./backend:/app'],
            'networks': ['app-network']
        }

        if depends_on:
            config['depends_on'] = depends_on
        
        return config

    def get_dockerfile_content(self):
        return '''FROM python:3.11-slim

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
'''

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        if components is None:
            components = []

        db_config = detect_database_service(components)
        
        if db_config:
            database_url = f'os.getenv("DATABASE_URL", "{db_config["url_template"]}")'
        else:
            database_url = '"sqlite:///./test.db"'

        config_content = f'''
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    DATABASE_URL: str = {database_url}
    SECRET_KEY: str = "your-secret-key-here"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
'''
        
        requirements = [
            'fastapi==0.104.1',
            'uvicorn[standard]==0.24.0',
            'python-multipart==0.0.6',
            'python-jose[cryptography]==3.3.0',
            'passlib[bcrypt]==1.7.4',
            'python-decouple==3.8',
            'pydantic-settings==2.0.3'
        ]
        if db_config:
            requirements.append(db_config['req']['fastapi'])

        return {
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
            'app/core/config.py': config_content,
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
            'requirements.txt': '\n'.join(requirements),
        }
