from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def show_error(message: str, suggestion: str = None):
    error_panel = Panel(
        f"❌ {message}\n\n {suggestion}" if suggestion else f"❌ {message}",
        title="Error",
        border_style="red"
    )
    console.print(error_panel)

def create_with_progress(description: str):
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    )

