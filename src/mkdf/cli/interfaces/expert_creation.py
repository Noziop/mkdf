import os
import typer
from pathlib import Path
from rich.console import Console

from ...core import create_from_template
from ..ui.panels import print_success_confirmation

console = Console()

def expert_create_mode(
    project_name: str,
    template_or_combo: str,
    components: list[str],
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
    project_path: str = ".",
    overwrite: bool = False
):
    # Si components est None :
    if components is None:
        
        return

    """Expert mode for project creation."""
    project_full_path = os.path.join(project_path, project_name)

    if Path(project_full_path).exists():
        if force:
            overwrite = True
            console.print("✨ Force overwrite enabled, proceeding...", style="green")
        elif typer.confirm(f"Directory '{project_full_path}' already exists. Overwrite?", default=False):
            console.print(f"⚠️  This will permanently DELETE all files in '{project_full_path}'", style="red")
            typer.confirm("Are you absolutely sure?", abort=True)
            overwrite = True
            console.print("✨ Proceeding with overwrite...", style="green")
        else:
            console.print("Project creation cancelled.", style="yellow")
            raise typer.Exit()
    else:
        overwrite = False

    port_config = {
        'backend': backend_port,
        'frontend': frontend_port,
        'database': db_port,
        'redis': redis_port,
        'subnet': subnet,
        'prometheus': prometheus_port,
        'grafana': grafana_port,
        'traefik_port': traefik_port,
        'traefik_dashboard_port': traefik_dashboard_port,
        'traefik_https_port': traefik_https_port,
    }
    if template_or_combo == 'docker':
        success = create_from_template(project_name, 'docker', components, base_path=project_path, port_config=port_config, overwrite=overwrite)
    else:
        success = create_from_template(project_name, template_or_combo, components, base_path=project_path, port_config=port_config, overwrite=overwrite)

    if success:
        full_path = os.path.join(project_path, project_name)
        template_type = 'docker' if template_or_combo == 'docker' else template_or_combo
        print_success_confirmation(project_name, full_path, template_type)
