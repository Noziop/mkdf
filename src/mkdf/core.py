import os
from .config.config_manager import ConfigManager
from .fs.brace_expansion import brace_expand
from .fs.path_analyzer import is_file_path
from .fs.dir_creator import create_directory
from .fs.file_creator import create_file
from .fs.fs_utils import is_path_safe  # Import for path safety check
from .templates.template_factory import TemplateFactory
from .utils import show_error, create_with_progress # Import for error and progress

config_manager = ConfigManager()

def create_simple_path(path: str):
    """Creates a simple file or directory based on the provided path."""
    if is_file_path(path):
        create_file(path)
    else:
        create_directory(path)

def create_from_pattern(pattern: str, overwrite: bool = False):
    """
    Creates a project structure from a brace expansion pattern.
    """
    try:
        expanded_paths = brace_expand(pattern)
        with create_with_progress("Creating project structure...") as progress:
            for path in expanded_paths:
                if is_file_path(path):
                    create_file(path, content="", overwrite=overwrite)
                else:
                    create_directory(path, overwrite=overwrite)
            progress.update(description="✅ Project created successfully!")
    except FileExistsError as e:
        show_error(f"Failed to create from pattern: {e}", "A file or directory already exists. Use --force to overwrite.")
    except Exception as e:
        show_error(f"Failed to create from pattern: {e}", "Please check your pattern syntax.")

def _create_from_template_recursive(base_path, template_dict, overwrite: bool = False):
    """
    Recursively creates directories and files from a template dictionary.
    """
    for name, content in template_dict.items():
        current_path = os.path.join(base_path, name)
        if isinstance(content, dict):
            create_directory(current_path, overwrite=overwrite)
            _create_from_template_recursive(current_path, content, overwrite=overwrite)
        elif content is None:
            create_directory(current_path, overwrite=overwrite)
        else:
            create_file(current_path, str(content), overwrite=overwrite)

def create_from_template(project_name, template_type, components=None, base_path=".", port_config=None, overwrite: bool = False):
    """Create project from template with optional port configuration"""
    if port_config is None:
        port_config = {}
    if 'subnet' not in port_config or port_config.get('subnet') is None:
        from .utils import find_free_subnet
        port_config['subnet'] = find_free_subnet(quiet=True)

    factory = TemplateFactory()
    project_path = os.path.join(base_path, project_name)
    try:
        if template_type == 'docker':
            from .templates.factories.docker_factory import DockerComposeFactory
            template = DockerComposeFactory.create(components, project_name, port_config)
        else:
            template = factory.create_template(template_type, components, project_name=project_name)
            
            # For template projects with multiple components, generate dynamic .env
            if components and isinstance(components, list) and len(components) > 1:
                from .templates.factories.env_factory import EnvFactory
                # Check if any components are databases or backends
                all_components = [template_type] + components
                has_backend = any(comp in EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Backend", []) for comp in all_components)
                has_database = any(comp in EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Database", []) for comp in all_components)
                
                if has_backend or has_database:
                    dynamic_env = EnvFactory.generate(all_components, project_name)
                    # Override the static .env with dynamic one
                    template['.env'] = dynamic_env

        create_directory(project_path, overwrite=overwrite)
        _create_from_template_recursive(project_path, template, overwrite=overwrite)
    except ValueError as e:
        show_error(f"Error creating project: {e}", "Please check the template type and components.")
        return False
    except Exception as e:
        show_error(f"An unexpected error occurred: {str(e)}", "Please try again or consult the documentation.")
        return False
    return True