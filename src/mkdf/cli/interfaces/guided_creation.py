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
from ..models.mappings import create_component_mapping
from ...templates.factories.env_factory import EnvFactory
from ...templates.template_factory import TEMPLATE_CATEGORIES

console = Console()

def guided_template_selection(project_name: str, project_path: str, overwrite: bool = False):
    """Guide user through template selection with Rich table"""
    print()
    show_templates_table()

    choice = typer.prompt("\nSelect template (name)", type=str)
    
    # Validate empty input
    if not choice.strip():
        typer.echo("❌ Error: No template selected. Please select a template.")
        raise typer.Exit(1)

    all_templates = [template for templates in TEMPLATE_CATEGORIES.values() for template in templates]

    if choice in all_templates:
        selected_template = choice
    else:
        typer.echo(f"❌ Error: Invalid choice: {choice}. Please choose from the available templates.")
        raise typer.Exit(1)

    # Clean UI separator before technical logs
    print("\n🚀 Creating your project...")
    
    create_from_template(project_name, selected_template, base_path=project_path, overwrite=overwrite)

    full_path = os.path.join(project_path, project_name)
    print_success_confirmation(project_name, full_path, selected_template)


def guided_docker_combo(project_name: str, project_path: str, overwrite: bool = False):
    """Guide user through Docker combo creation"""
    print()
    show_docker_components_table()

    components_input = typer.prompt("\nSelect components (space-separated)", type=str)
    
    # Validate empty input
    if not components_input.strip():
        typer.echo("❌ Error: No components selected. Please select at least one component.")
        raise typer.Exit(1)
    
    components_raw = components_input.split()

    # Create component mapping for number-to-name conversion
    component_map = create_component_mapping()
    
    # Convert numbers to component names if needed
    components = []
    invalid_inputs = []
    
    for component in components_raw:
        component = component.strip()
        if component in component_map:
            components.append(component_map[component])
        else:
            # Check if it's a valid number but out of range
            if component.isdigit():
                num = int(component)
                max_num = len([c for cat in EnvFactory.DOCKER_COMPONENT_CATEGORIES.values() for c in cat])
                if num < 1 or num > max_num:
                    invalid_inputs.append(component)
                else:
                    # This should not happen if mapping is correct, but safety check
                    invalid_inputs.append(component)
            else:
                # Check if it's an invalid component name
                all_docker_components = [component for components_list in EnvFactory.DOCKER_COMPONENT_CATEGORIES.values() for component in components_list]
                if component not in all_docker_components:
                    invalid_inputs.append(component)
                else:
                    components.append(component)

    # Check for invalid inputs
    if invalid_inputs:
        typer.echo(f"❌ Error: Invalid components: {', '.join(invalid_inputs)}. Please choose from the available list.")
        raise typer.Exit(1)

    valid_components = components
    if not valid_components:
        typer.echo("❌ Error: No valid components found. Please try again.")
        raise typer.Exit(1)

    # Add clean spacing before ports question
    print()
    custom_ports = typer.confirm("Configure custom ports?", default=False)

    port_config = {}
    if custom_ports:
        port_config = get_interactive_port_config()

    # Clean UI separator before technical logs
    print("\n🚀 Creating your project...")
    
    create_from_template(project_name, 'docker', valid_components, base_path=project_path, port_config=port_config, overwrite=overwrite)

    full_path = os.path.join(project_path, project_name)
    print_success_confirmation(project_name, full_path, 'docker')

def guided_create_mode(project_name: str = None, force: bool = False):
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
        if force:
            overwrite = True
            console.print("✨ Force overwrite enabled, proceeding...", style="green")
        elif typer.confirm(f"Directory '{full_project_path}' already exists. Overwrite?", default=False):
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
