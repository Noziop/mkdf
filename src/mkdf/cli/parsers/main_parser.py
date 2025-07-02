import typer
from typing import Optional, List

from ..commands.create import create_command
from ..commands.interactive import interactive_command

app = typer.Typer(
    name="mkdf",
    help="MKDF - Professional project structure creator.",
    epilog=(
        "Examples:\n"
        "  mkdf myapp/{src/,docs/readme.md}      # Direct structure creation (no command)\n"
        "  mkdf create myapp fastapi             # Create from template\n"
        "  mkdf web                              # Launch web interface\n"
        "  mkdf -i                               # Interactive mode\n"
        "\nNote: COMMAND is optional. If omitted, you can use patterns or interactive mode."
    ),
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
    backend_port: int = typer.Option(None, "--backend-port", help="Backend service port"),
    frontend_port: int = typer.Option(None, "--frontend-port", help="Frontend service port"),
    db_port: int = typer.Option(None, "--db-port", help="Database port (auto-detect if not specified)"),
    redis_port: int = typer.Option(None, "--redis-port", help="Redis port"),
    subnet: str = typer.Option(None, "--subnet", help="Docker network subnet"),
    prometheus_port: int = typer.Option(None, "--prometheus-port", help="Prometheus port"),
    grafana_port: int = typer.Option(None, "--grafana-port", help="Grafana port"),
    traefik_port: int = typer.Option(None, "--traefik-port", help="Traefik HTTP port"),
    traefik_https_port: int = typer.Option(None, "--traefik-https-port", help="Traefik HTTPS port"),
    traefik_dashboard_port: int = typer.Option(None, "--traefik-dashboard-port", help="Traefik dashboard port")
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
        traefik_https_port,
        traefik_dashboard_port
    )

@app.callback()
def main(
    ctx: typer.Context,
    i: bool = typer.Option(False, "-i", "--interactive", help="Launch interactive mode"),
):
    """MKDF - Professional project structure creator.
    This tool allows you to create complex project structures with ease, using templates or Docker combos.
    mkdf can also be used in interactive mode for guided project creation.
    usage: mdkf => launch interactive mode
    usage: mkdf create <project_name> <template_or_combo> [components...] => create a new project from template or Docker combo
    usage: mkdf web => launch the web interface for MKDF
    """
    if ctx.invoked_subcommand is not None:
        return
    if i:
        interactive_command()
        raise typer.Exit()
    interactive_command()
    raise typer.Exit()
