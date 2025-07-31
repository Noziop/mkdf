from typing import Optional, List
from ..interfaces.guided_creation import guided_create_mode
from ..interfaces.expert_creation import expert_create_mode
from ...config.config_manager import ConfigManager
from ...utils import find_free_subnet, find_free_port

config_manager = ConfigManager()

def create_command(
    project_name: Optional[str],
    template_or_combo: Optional[str],
    components: Optional[List[str]],
    force: bool,
    verbose: bool,
    backend_port: int,
    frontend_port: int,
    db_port: int,
    redis_port: int,
    subnet: str,
    prometheus_port: int,
    grafana_port: int,
    traefik_port: int,
    traefik_dashboard_port: int,
    traefik_https_port: int,
):
    # Early exit for guided mode - no need to compute ports yet
    if project_name is None:
        return guided_create_mode(force=force)

    if template_or_combo is None:
        return guided_create_mode(project_name=project_name, force=force)

    # Handle 'preferred' template
    if template_or_combo == "preferred":
        preferred_templates = config_manager.get("preferred_templates", {})
        backend = preferred_templates.get("backend")
        frontend = preferred_templates.get("frontend")
        fullstack = preferred_templates.get("fullstack")

        # Prioritize fullstack if available, otherwise combine backend and frontend
        if fullstack:
            template_or_combo = fullstack
            components = None # Fullstack templates usually don't take components directly
        elif backend and frontend:
            template_or_combo = "docker" # Assuming preferred backend/frontend implies a docker combo
            components = [backend, frontend]
        elif backend:
            template_or_combo = backend
            components = None
        elif frontend:
            template_or_combo = frontend
            components = None
        else:
            print("No preferred templates configured. Falling back to guided mode.")
            return guided_create_mode(project_name=project_name)

    # Handle 'preferred-combo'
    elif template_or_combo == "preferred-combo":
        preferred_combo_str = config_manager.get("preferred_docker_combo")
        if preferred_combo_str:
            template_or_combo = "docker"
            components = preferred_combo_str.split() # Split the string into a list of components
        else:
            print("No preferred Docker combo configured. Falling back to guided mode.")
            return guided_create_mode(project_name=project_name)

    # Now that we know the project type, calculate ports only for Docker projects
    if template_or_combo == "docker":
        if subnet is None:
            subnet = find_free_subnet(quiet=True)

        # Define default port values for various services
        default_port_values = {
            'backend': 8000,
            'frontend': 3000,
            'redis': 6379,
            'prometheus': 9090,
            'grafana': 3001,
            'traefik': 8080,
            'traefik_dashboard': 8090,
            'traefik_https': 8085
        }

        # Assign free ports if not explicitly provided by the user
        if backend_port is None:
            backend_port = find_free_port(default_port_values['backend'])
        if frontend_port is None:
            frontend_port = find_free_port(default_port_values['frontend'])
        if db_port is None:
            db_port = None  # Will be auto-detected in the factory
        if redis_port is None:
            redis_port = find_free_port(default_port_values['redis'])
        if prometheus_port is None:
            prometheus_port = find_free_port(default_port_values['prometheus'])
        if grafana_port is None:
            grafana_port = find_free_port(default_port_values['grafana'])
        if traefik_port is None:
            traefik_port = find_free_port(default_port_values['traefik'])
        if traefik_dashboard_port is None:
            traefik_dashboard_port = find_free_port(default_port_values['traefik_dashboard'])
        if traefik_https_port is None:
            traefik_https_port = find_free_port(default_port_values['traefik_https'])
    else:
        # For non-Docker projects, we don't need most of these ports
        # Keep the provided values or set reasonable defaults
        if subnet is None:
            subnet = "172.18.0.0/16"  # Default subnet, won't be used anyway

    expert_create_mode(
        project_name,
        template_or_combo,
        components,
        force,
        verbose,
        backend_port,
        frontend_port,
        db_port,
        redis_port,
        subnet,
        prometheus_port,
        grafana_port,
        traefik_port,
        traefik_dashboard_port,
        traefik_https_port,
        overwrite=force
    )
