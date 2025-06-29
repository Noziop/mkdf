import typer
from typing import Optional, List

from ..commands.create import create_command
from ..commands.web import web_command
from ..commands.interactive import interactive_command
from ..commands.pattern import pattern_command

app = typer.Typer(
    name="mkdf",
    help=" MKDF - Professional project structure creator",
    add_completion=False,
    invoke_without_command=True,
)

@app.command()
def create(
    project_name: Optional[str] = typer.Argument(None, help="Project name (optional - launches guided mode if omitted)"),
    template_or_combo: Optional[str] = typer.Argument(None, help="Template name or 'docker' for combo"),
    components: Optional[List[str]] = typer.Argument(None, help="Docker components for combo"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force overwrite existing files"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    backend_port: int = typer.Option(8000, "--backend-port", help="Backend service port"),
    frontend_port: int = typer.Option(3000, "--frontend-port", help="Frontend service port"),
    db_port: int = typer.Option(None, "--db-port", help="Database port (auto-detect if not specified)"),
    redis_port: int = typer.Option(6379, "--redis-port", help="Redis port"),
    subnet: str = typer.Option(None, "--subnet", help="Docker network subnet"),
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
    create_command(
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
    web_command()


@app.command("interactive", help="Launch interactive mode")
def interactive_cmd():
    """Launch interactive mode"""
    interactive_command()


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
    if ctx.invoked_subcommand is not None:
        return

    interactive_command()
    raise typer.Exit()


@app.command("pattern")
def pattern_create(
    pattern: str = typer.Argument(
        ..., help="Brace expansion pattern to create directories and files"
    )
):
    """ Create directories and files from a brace expansion pattern"""
    pattern_command(pattern)
