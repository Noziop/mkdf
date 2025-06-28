from typing import Optional, List
from ..interfaces.guided_creation import guided_create_mode
from ..interfaces.expert_creation import expert_create_mode

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
