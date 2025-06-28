import os
import typer
from pathlib import Path
from rich.console import Console
import click

from ..ui.tables import show_templates_table, show_docker_components_table
from ..ui.panels import print_success_confirmation
from ...core import create_from_template
from ..validators.path import get_project_path
from ..models.ports import get_interactive_port_config
from ...templates.factories.env_factory import EnvFactory
from ...templates.template_factory import TEMPLATE_CATEGORIES

console = Console()

def guided_template_selection(project_name: str, project_path: str, overwrite: bool = False):
    """Guide user through template selection with Rich table"""
    print()
    show_templates_table()

    choice = typer.prompt("\nSelect template (name)", type=str)

    all_templates = [template for templates in TEMPLATE_CATEGORIES.values() for template in templates]

    if choice in all_templates:
        selected_template = choice
    else:
        typer.echo(f"Invalid choice: {choice}")
        return

    create_from_template(project_name, selected_template, base_path=project_path, overwrite=overwrite)

    full_path = os.path.join(project_path, project_name)
    print_success_confirmation(project_name, full_path, selected_template)


def guided_docker_combo(project_name: str, project_path: str, overwrite: bool = False):
    """Guide user through Docker combo creation"""
    print()
    show_docker_components_table()

    components_input = typer.prompt("\nSelect components (space-separated)", type=str)
    components = components_input.split()

    all_docker_components = [component for components_list in EnvFactory.DOCKER_COMPONENT_CATEGORIES.values() for component in components_list]
    valid_components = [c for c in components if c in all_docker_components]
    if len(valid_components) != len(components):
        invalid = set(components) - set(all_docker_components)
        typer.echo(f"Invalid components: {', '.join(invalid)}. Please choose from the available list.")
        return

    custom_ports = typer.confirm("Configure custom ports?", default=False)

    port_config = {}
    if custom_ports:
        port_config = get_interactive_port_config()

    create_from_template(project_name, 'docker', valid_components, base_path=project_path, port_config=port_config, overwrite=overwrite)

    full_path = os.path.join(project_path, project_name)
    print_success_confirmation(project_name, full_path, 'docker')

def guided_create_mode(project_name: str = None):
    """Guided project creation with simple prompts"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(" MKDF Guided Project Creator")
    print()

    if not project_name:
        project_name = typer.prompt("Project name")

    project_path = get_project_path()

    full_project_path = os.path.join(project_path, project_name)
    console.print(f"Will create project at: {full_project_path}", style="orange1")

    overwrite = False
    if Path(full_project_path).exists():
        if typer.confirm(f"Directory '{full_project_path}' already exists. Overwrite?", default=False):
            console.print(f"⚠️  This will permanently DELETE all files in '{full_project_path}'", style="red")
            typer.confirm("Are you absolutely sure?", abort=True)
            overwrite = True
            console.print("✨ Proceeding with overwrite...", style="green")
        else:
            console.print("Project creation cancelled.", style="yellow")
            raise typer.Exit()

    mode = typer.prompt(
        "Template or Docker combo",
        type=click.Choice(['template', 'docker', 't', 'd']),
        show_choices=True
    )

    if mode in ['docker', 'd']:
        guided_docker_combo(project_name, project_path, overwrite=overwrite)
    else:
        guided_template_selection(project_name, project_path, overwrite=overwrite)
