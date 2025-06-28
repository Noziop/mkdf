import json
from pathlib import Path
import logging
from typing import Dict, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_DIR = Path.home() / '.config' / 'mkdf'
CONFIG_FILE = CONFIG_DIR / 'config.json'
TEMPLATES_FILE = CONFIG_DIR / 'templates.json'
DEFAULTS_FILE = CONFIG_DIR / 'defaults.json'
WEB_FILE = CONFIG_DIR / 'web.json'

class ConfigManager:
    def __init__(self) -> None:
        self.config: Dict[str, Any] = self._load_default_config()
        self.config.update(self._load_user_config())

    def _load_default_config(self) -> Dict[str, Any]:
        # Define default configuration values
        return {
            "default_project_path": str(Path.home() / "projects"),
            "templates_dir": str(CONFIG_DIR / "templates"),
            "web_port_start": 9500,
            "enable_logging": True,
            "log_level": "INFO",
            "author_name": "Your Name",
            "author_email": "your.email@example.com",
            "preferred_templates": {
                "backend": "fastapi",
                "frontend": "vue",
                "fullstack": "nextjs"
            }
        }

    def _load_user_config(self) -> Dict[str, Any]:
        if not CONFIG_FILE.exists():
            return {}
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding config.json: {e}")
            return {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self._save_user_config()

    def _save_user_config(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            logging.error(f"Error saving config.json: {e}")

def load_config(file_path: Path) -> Dict[str, Any]:
    """Loads a JSON configuration file."""
    if not file_path.exists():
        return {}
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding {file_path.name}: {e}")
        return {}
    except IOError as e:
        logging.error(f"Error reading {file_path.name}: {e}")
        return {}

def save_config(data: Dict[str, Any], file_path: Path) -> None:
    """Saves data to a JSON configuration file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        logging.error(f"Error saving {file_path.name}: {e}")