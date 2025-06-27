import os
import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from pathlib import Path

from ..core import create_from_template, create_from_pattern
from ..web.server import run_server
from .interactive import start_interactive_mode

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


@app.command()
def create(
    project_name: str = typer.Argument(..., help="Project name"),
    template: str = typer.Argument(..., help="Template type"),
    components: Optional[List[str]] = typer.Argument(
        None, help="Additional components"
    ),
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
    """️ Create a new project from template"""
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
    create_from_template(project_name, template, components, port_config=port_config)


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

