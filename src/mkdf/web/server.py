

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Field, Session, create_engine
from pathlib import Path
import os
from typing import Optional, List
from datetime import datetime

# --- Database Setup ---
DB_PATH = Path.home() / ".config" / "mkdf" / "web.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --- FastAPI Models ---
class WebConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    theme: str = "dark"
    preferred_templates: str = ""
    last_project_path: str = ""

class ProjectHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    template: str
    created_at: datetime
    path: str

# --- FastAPI App ---
app = FastAPI()


# --- Dependency ---
def get_db():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- API Endpoints ---
@app.get("/api/themes")
async def get_themes():
    return {
        "artistic": ["8bit", "cyberpunk", "dark", "girly", "light", "manga"],
        "seasonal": [],
        "mood": []
    }

@app.post("/api/config/theme")
async def set_theme(theme: str, db: Session = Depends(get_db)):
    config = db.query(WebConfig).first()
    if not config:
        config = WebConfig(theme=theme)
        db.add(config)
    else:
        config.theme = theme
    db.commit()
    db.refresh(config)
    return {"message": f"Theme set to {theme}"}

# --- Preserve existing functionality ---
from ..core import create_from_template
from ..templates.template_factory import TemplateFactory
from ..fs.brace_expansion import brace_expand
from ..fs.path_analyzer import is_file_path
from ..fs.dir_creator import create_directory
from ..fs.file_creator import create_file

@app.get("/api/templates")
async def get_templates():
    """Get available templates from factories"""
    try:
        factory = TemplateFactory()
        templates = factory.get_all_templates()
        
        return {json_key: templates[json_key] for json_key in templates.keys() if json_key != 'docker'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching templates: {e}")


@app.post('/preview_pattern')
def preview_pattern(data: dict):
    pattern = data.get('pattern', '')
    try:
        expanded_paths = brace_expand(pattern)
        # This is a simplified tree generation.
        # The original implementation can be adapted if needed.
        tree_string = "\n".join(expanded_paths)
        return {"success": True, "tree": tree_string}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post('/create_pattern')
def create_pattern_web(data: dict):
    pattern = data.get('pattern', '')
    try:
        expanded_paths = brace_expand(pattern)
        for path in expanded_paths:
            if is_file_path(path):
                create_file(path)
            else:
                create_directory(path)
        return {"message": "Project structure created successfully!", "success": True}
    except Exception as e:
        return {"message": f"Error creating project: {e}", "success": False}

@app.post('/create_template')
def create_template_web(data: dict):
    project_name = data.get('project_name', '')
    template_type = data.get('template_type', '')
    try:
        create_from_template(project_name, template_type, overwrite=True)
        return {"message": f"Successfully created project '{project_name}' from template '{template_type}'.", "success": True}
    except ValueError as e:
        return {"message": f"Error: {e}", "success": False}
    except Exception as e:
        return {"message": f"An unexpected error occurred: {e}", "success": False}

@app.post('/preview_docker_compose')
def preview_docker_compose(data: dict):
    components = data.get('components', [])
    factory = TemplateFactory()
    try:
        template = factory.create_template('docker', components)
        compose_yml = template.get('docker-compose.yml', '# No docker-compose.yml generated')
        return {"success": True, "compose_yml": compose_yml}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post('/create_docker')
def create_docker_web(data: dict):
    project_name = data.get('project_name', '')
    components = data.get('components', [])
    try:
        create_from_template(project_name, 'docker', components, overwrite=True)
        return {"message": f"Successfully created Docker project '{project_name}' with components {components}.", "success": True}
    except ValueError as e:
        return {"message": f"Error: {e}", "success": False}
    except Exception as e:
        return {"message": f"An unexpected error occurred: {e}", "success": False}

# --- Static Files ---
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="spa")
