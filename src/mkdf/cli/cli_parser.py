import os
import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from pathlib import Path
import click # Added for typer.prompt with click.Choice

from ..core import create_from_template, create_from_pattern
from ..web.server import run_server
from .interactive import start_interactive_mode, show_docker_components_table
from ..templates.template_factory import TEMPLATE_CATEGORIES
from ..templates.docker_templates import DOCKER_COMPONENT_CATEGORIES

app = typer.Typer(
    name="mkdf",
    help=" MKDF - Professional project structure creator",
    add_completion=False,
    invoke_without_command=True,
)

console = Console()

def clear_screen():
    """Clear the terminal screen - cross-platform"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/macOS
        os.system('clear')

def show_rainbow_banner():
    clear_screen()
    print()
    console = Console()

    # Read ASCII art from external file
    banner_file = Path(__file__).parent / "banner.txt"

    try:
        with open(banner_file, 'r', encoding='utf-8') as f:
            ascii_lines = [line.rstrip() for line in f.readlines()]
    except FileNotFoundError:
        # Fallback if file not found
        ascii_lines = ["MKDF - File not found"]

    # Rainbow Pride colors
    pride_colors = ["red", "orange3", "yellow", "green", "blue", "purple"]

    for i, line in enumerate(ascii_lines):
        if line.strip():  # Skip empty lines
            color = pride_colors[i % len(pride_colors)]
            console.print(line, style=f"bold {color}")

    print()  # Add an extra newline for spacing
    console.print("━" * 90, style="bright_blue")
    console.print("️‍ Make Directories and Files - Professional Project Creator - By github.com/Noziop", style="dim")
    console.print("━" * 90, style="bright_blue")


def run_interactive_session():
    """Displays banner and starts interactive mode."""
    start_interactive_mode(banner_callback=show_rainbow_banner)

def show_templates_table():
    """Display available templates in a beautiful Rich table"""
    console = Console()

    # Template categories (matching existing structure)
    TEMPLATE_CATEGORIES = {
        "Backend API": ["fastapi", "flask", "express", "gofiber"],
        "Frontend": ["vue", "react", "svelte", "angular", "nextjs", "nuxtjs"],
        "Fullstack": ["laravel", "django", "symfony"],
        "Static": ["simple", "static"],
        "Mobile": ["react-native", "flutter"],
        "Desktop": ["electron", "tauri"]
    }

    table = Table(title=" Available Templates", show_header=True, header_style="bold magenta")

    # Add columns for each category (neutral white style)
    table.add_column("Backend API", justify="center", style="white", width=12)
    table.add_column("Frontend", justify="center", style="white", width=10)
    table.add_column("Fullstack", justify="center", style="white", width=10)
    table.add_column("Static", justify="center", style="white", width=10)
    table.add_column("Mobile", justify="center", style="white", width=12)
    table.add_column("Desktop", justify="center", style="white", width=10)

    # Create rows by filling each category column
    max_items = max(len(templates) for templates in TEMPLATE_CATEGORIES.values())

    for i in range(max_items):
        row = []
        for category, templates in TEMPLATE_CATEGORIES.items():
            if i < len(templates):
                row.append(templates[i])
            else:
                row.append("")
        table.add_row(*row)

    console.print(table)

def _create_from_template_wrapper(project_name: str, template_type: str, components: Optional[List[str]] = None, port_config: Optional[dict] = None, project_path: str = "."):
    """Wrapper to call create_from_template with collected arguments."""
    create_from_template(project_name, template_type, components, base_path=project_path, port_config=port_config)

def _create_docker_combo_wrapper(project_name: str, components: List[str], port_config: Optional[dict] = None, project_path: str = "."):
    """Wrapper to call create_from_template for Docker combos."""
    _create_from_template_wrapper(project_name, 'docker', components, port_config, project_path=project_path)

def guided_template_selection(project_name: str, project_path: str):
    """Guide user through template selection with Rich table"""
    print()
    show_templates_table() # Use Rich table instead of plain list

    # Keep existing prompt logic
    choice = typer.prompt("\nSelect template (name)", type=str)

    all_templates = [template for templates in TEMPLATE_CATEGORIES.values() for template in templates]

    if choice in all_templates:
        selected_template = choice
    else:
        typer.echo(f"Invalid choice: {choice}")
        return

    _create_from_template_wrapper(project_name, selected_template, project_path=project_path)

def guided_docker_combo(project_name: str, project_path: str):
    """Guide user through Docker combo creation"""
    print()
    show_docker_components_table()

    components_input = typer.prompt("\nSelect components (space-separated)", type=str)
    components = components_input.split()

    # Validate components
    all_docker_components = [component for components_list in DOCKER_COMPONENT_CATEGORIES.values() for component in components_list]
    valid_components = [c for c in components if c in all_docker_components]
    if len(valid_components) != len(components):
        invalid = set(components) - set(all_docker_components)
        typer.echo(f"Invalid components: {', '.join(invalid)}. Please choose from the available list.")
        return

    custom_ports = typer.confirm("Configure custom ports?", default=False)

    port_config = {}
    if custom_ports:
        port_config['backend'] = typer.prompt("Backend port", default=8000, type=int)
        port_config['frontend'] = typer.prompt("Frontend port", default=3000, type=int)
        port_config['database'] = typer.prompt("Database port", default=5432, type=int)
        port_config['redis'] = typer.prompt("Redis port", default=6379, type=int)
        port_config['subnet'] = typer.prompt("Docker network subnet", default="172.18.0.0/16", type=str)
        port_config['prometheus'] = typer.prompt("Prometheus port", default=9090, type=int)
        port_config['grafana'] = typer.prompt("Grafana port", default=3001, type=int)
        port_config['traefik'] = typer.prompt("Traefik HTTP port", default=80, type=int)
        port_config['traefik_dashboard'] = typer.prompt("Traefik dashboard port", default=8080, type=int)


    _create_docker_combo_wrapper(project_name, valid_components, port_config, project_path=project_path)

def guided_create_mode(project_name: Optional[str] = None):
    """Guided project creation with simple prompts"""
    clear_screen()
    print(" MKDF Guided Project Creator")
    print()

    # Step 1: Project name
    if not project_name:
        project_name = typer.prompt("Project name")

    # Step 2: Project path
    default_path = str(Path.home() / "projects")
    project_path_input = typer.prompt("Project path", default=default_path)

    # Expand user tilde first, as os.path.isabs doesn't handle it.
    expanded_path = os.path.expanduser(project_path_input)

    # If the path is absolute, use it. Otherwise, join with the default path.
    if os.path.isabs(expanded_path):
        final_path = expanded_path
    else:
        final_path = os.path.join(default_path, expanded_path)

    # Normalize to get a clean, absolute path
    project_path = os.path.abspath(final_path)
    typer.echo(f"Will create project at: {os.path.join(project_path, project_name)}")

    # Step 2: Template or Docker combo choice
    mode = typer.prompt(
        "Template or Docker combo",
        type=click.Choice(['template', 'docker', 't', 'd']),
        show_choices=True
    )

    if mode in ['docker', 'd']:
        guided_docker_combo(project_name, project_path)
    else:
        guided_template_selection(project_name, project_path)

def expert_create_mode(
    project_name: str,
    template_or_combo: str,
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
    traefik_dashboard_port: int
):
    """Expert mode for project creation."""
    port_config = {
        'backend': backend_port,
        'frontend': frontend_port,
        'database': db_port,
        'redis': redis_port,
        'subnet': subnet,
        'prometheus': prometheus_port,
        'grafana': grafana_port,
        'traefik': traefik_port,
        'traefik_dashboard': traefik_dashboard_port,
    }
    if template_or_combo == 'docker':
        _create_docker_combo_wrapper(project_name, components, port_config)
    else:
        _create_from_template_wrapper(project_name, template_or_combo, components, port_config)


@app.command()
def create(
    project_name: Optional[str] = typer.Argument(None, help="Project name (optional - launches guided mode if omitted)"),
    template_or_combo: Optional[str] = typer.Argument(None, help="Template name or 'docker' for combo"),
    components: Optional[List[str]] = typer.Argument(None, help="Docker components for combo"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force overwrite existing files"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    # NEW PORT OPTIONS
    backend_port: int = typer.Option(8000, "--backend-port", help="Backend service port"),
    frontend_port: int = typer.Option(3000, "--frontend-port", help="Frontend service port"),
    db_port: int = typer.Option(None, "--db-port", help="Database port (auto-detect if not specified)"),
    redis_port: int = typer.Option(6379, "--redis-port", help="Redis port"),

    # NEW NETWORK OPTIONS
    subnet: str = typer.Option("172.18.0.0/16", "--subnet", help="Docker network subnet"),

    # NEW MONITORING PORTS
    prometheus_port: int = typer.Option(9090, "--prometheus-port", help="Prometheus port"),
    grafana_port: int = typer.Option(3001, "--grafana-port", help="Grafana port"),
    traefik_port: int = typer.Option(80, "--traefik-port", help="Traefik HTTP port"),
    traefik_dashboard_port: int = typer.Option(8080, "--traefik-dashboard-port", help="Traefik dashboard port")
):
    """
    Create a new project from template or Docker combo.

    Examples:
        mkdf create                           # Guided mode (interactive prompts)
        mkdf create myapp simple              # Expert mode (direct creation)  
        mkdf create myapi docker fastapi vue  # Expert mode (Docker combo)
    """
    # Guided mode if no project name provided
    if project_name is None:
        return guided_create_mode()

    # If partial arguments -> Continue guided mode with prefilled values
    if template_or_combo is None:
        return guided_create_mode(project_name=project_name)

    # If all arguments -> Expert mode (existing functionality)
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
        traefik_dashboard_port
    )


@app.command("web")
def start_web():
    """ Start the web interface"""
    run_server()


@app.command("interactive", help="Launch interactive mode")
def interactive_command():
    """Launch interactive mode"""
    run_interactive_session()


@app.callback()
def main(
    ctx: typer.Context,
    i: bool = typer.Option(
        False, "-i", "--interactive", help="Launch interactive mode"
    ),
):
    """
    Main callback to handle top-level options and commands.
    """
    # If a command is invoked (like 'create', 'web', etc.), let it run.
    # The 'interactive' command will call run_interactive_session itself.
    if ctx.invoked_subcommand is not None:
        return

    # This handles `mkdf` (no command) and `mkdf -i`.
    run_interactive_session()
    # The interactive session is blocking. When the user exits it,
    # we raise typer.Exit() to prevent Typer from showing the default help message.
    raise typer.Exit()


@app.command("pattern")
def pattern_create(
    pattern: str = typer.Argument(
        ..., help="Brace expansion pattern to create directories and files"
    )
):
    """ Create directories and files from a brace expansion pattern"""
    create_from_pattern(pattern)


def enhanced_interactive_mode():
    show_rainbow_banner()

    table = Table(title=" Available Actions")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    table.add_row("1", " Create from pattern (brace expansion)")
    table.add_row("2", " Create from template")
    table.add_row("3", " Create Docker combo")
    table.add_row("4", " Launch web interface")
    table.add_row("5", "⚙️ Configuration")
    table.add_row("0", " Exit")

    console.print(table)

