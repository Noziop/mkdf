from pydantic_settings import BaseSettings
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
