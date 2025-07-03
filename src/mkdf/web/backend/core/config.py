# backend/core/config.py
from pydantic_settings import BaseSettings
from pathlib import Path
import json
import logging
from logging.handlers import RotatingFileHandler
from mkdf.utils import find_free_port

class Settings(BaseSettings):
    # Default values (fallbacks)
    web_port_start: int = 9500
    enable_logging: bool = True
    log_level: str = "INFO"
    author_name: str = "Anonymous"
    author_email: str = "user@example.com"
    default_project_path: str = "/tmp"
    templates_dir: str = ""
    
    # Web specific
    debug_mode: bool = True
    auth_enabled: bool = False
    cors_origins: list = ["http://localhost:3000"]
    
    def __init__(self, **kwargs):
        # Charger le config.json existant FIRST !
        config_file = Path.home() / ".config" / "mkdf" / "config.json"
        config_data = {}
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        
        # Merge avec les kwargs
        merged_data = {**config_data, **kwargs}
        super().__init__(**merged_data)
        
        # Setup logging avec les vraies valeurs
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging avec les settings du config.json"""
        if not self.enable_logging:
            return
            
        logs_dir = Path.home() / ".config" / "mkdf" / "web" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / "mkdf-web.log"
        
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=1_000_000,
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        
        logging.basicConfig(
            level=getattr(logging, self.log_level.upper()),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                file_handler
            ]
        )
    
    def get_backend_port(self):
        """Port backend avec scan à partir de web_port_start"""
        return find_free_port(self.web_port_start)
    
    def get_frontend_port(self):
        """Port frontend avec scan à partir de 3000"""
        return find_free_port(3000)
    
    @property
    def cors_origins_dynamic(self):
        """CORS origins avec port frontend dynamique"""
        frontend_port = self.get_frontend_port()
        return [f"http://localhost:{frontend_port}"]
    
    class Config:
        env_prefix = "MKDF_"  # Pour override avec variables d'env si besoin
