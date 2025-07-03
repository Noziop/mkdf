# backend/database.py
from sqlmodel import SQLModel, Session, create_engine
from pathlib import Path
import logging

# Garde ta DB existante - IMPORTANT !
DB_PATH = Path.home() / ".config" / "mkdf" / "web.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Connection avec echo depuis config
from .config import Settings
settings = Settings()

engine = create_engine(
    DATABASE_URL, 
    echo=settings.debug_mode  # Logs SQL si debug
)

def create_db_and_tables():
    """Crée les tables si elles n'existent pas"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency injection pour FastAPI"""
    with Session(engine) as session:
        yield session
