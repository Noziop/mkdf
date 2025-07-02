from rich.console import Console
from rich.panel import Panel

def print_success_confirmation(project_name: str, project_path: str, template_type: str):
    """Print a friendly success message after project creation"""
    from rich.console import Console
    from rich.panel import Panel

    console = Console()

    success_text = f" You're all set! Better get yourself coding this brilliant idea of yours!\n\n"
    success_text += f" Project '{project_name}' created successfully!"
    success_text += f"\n Location: {project_path}"

    if template_type == 'django':
        next_steps = "Next steps:\n  cd " + project_path + "\n  pip install -r requirements.txt\n  python manage.py runserver"
    elif template_type == 'vue':
        next_steps = "Next steps:\n  cd " + project_path + "\n  npm install\n  npm run dev"
    elif template_type == 'fastapi':
        next_steps = "Next steps:\n  cd " + project_path + "\n  pip install -r requirements.txt\n  python main.py"
    elif template_type == 'docker':
        next_steps = "Next steps:\n  cd " + project_path + "\n  docker-compose up -d\n  # Then follow your README for service details"
    elif template_type == 'custom':
        next_steps = "Next steps:\n  cd " + project_path + "\n  Happy coding! 🚀"
    else:
        next_steps = "Next steps:\n  cd " + project_path + "\n  Start coding!"

    panel_content = success_text + "\n\n" + next_steps
    panel = Panel(panel_content, title="✨ Project Created Successfully", border_style="green")
    console.print(panel)


