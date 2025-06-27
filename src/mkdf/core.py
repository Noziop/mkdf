import os
from .config.config_manager import ConfigManager
from .fs.brace_expansion import brace_expand
from .fs.path_analyzer import is_file_path
from .fs.dir_creator import create_directory
from .fs.file_creator import create_file
from .templates.template_factory import TemplateFactory
from .utils import show_error, create_with_progress # Import for error and progress

config_manager = ConfigManager()

def create_from_pattern(pattern: str):
    """
    Creates a project structure from a brace expansion pattern.
    """
    try:
        expanded_paths = brace_expand(pattern)
        with create_with_progress("Creating project structure...") as progress:
            for path in expanded_paths:
                if is_file_path(path):
                    create_file(path)
                else:
                    create_directory(path)
            progress.update(description="✅ Project created successfully!")
    except Exception as e:
        show_error(f"Failed to create from pattern: {e}", "Please check your pattern syntax.")

def _create_from_template_recursive(base_path, template_dict):
    """
    Recursively creates directories and files from a template dictionary.
    """
    for name, content in template_dict.items():
        current_path = os.path.join(base_path, name)
        if isinstance(content, dict):
            create_directory(current_path)
            _create_from_template_recursive(current_path, content)
        elif content is None:
            create_directory(current_path)
        else:
            create_file(current_path, str(content))

def create_from_template(project_name, template_type, components=None, base_path=".", port_config=None):
    """Create project from template with optional port configuration"""
    if port_config is None:
        port_config = {
            'backend': 8000,
            'frontend': 3000,
            'database': None, # This will be auto-detected by get_docker_template
            'redis': 6379,
            'subnet': '172.18.0.0/16',
            'prometheus': 9090,
            'grafana': 3001,
            'traefik': 80,
            'traefik_dashboard': 8080,
        }

    factory = TemplateFactory()
    project_path = os.path.join(base_path, project_name)
    try:
        if template_type == 'docker':
            from .templates.docker_templates import get_docker_template
            template = get_docker_template(components, project_name, port_config)
        else:
            template = factory.create_template(template_type, components)

        create_directory(project_path)
        _create_from_template_recursive(project_path, template)
        print(f"Successfully created project '{project_name}' from template '{template_type}'.")
    except ValueError as e:
        show_error(f"Error creating project: {e}", "Please check the template type and components.")
    except Exception as e:
        show_error(f"An unexpected error occurred: {e}", "Please try again or consult the documentation.")