from typing import Optional, List
from ..interfaces.guided_creation import guided_create_mode
from ..interfaces.expert_creation import expert_create_mode
from ...config.config_manager import ConfigManager

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
):
    if project_name is None:
        return guided_create_mode()

    if template_or_combo is None:
        return guided_create_mode(project_name=project_name)

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
        overwrite=force
    )
