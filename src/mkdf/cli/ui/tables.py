from rich.console import Console
from rich.table import Table

from ...templates.template_factory import TEMPLATE_CATEGORIES
from ...templates.factories.env_factory import EnvFactory
from ..models.mappings import create_template_mapping

def show_templates_table():
    """Display available templates in a beautiful Rich table"""
    console = Console()

    table = Table(title=" Available Templates", show_header=True, header_style="bold white")

    table.add_column("Backend API", justify="center", style="white", width=12)
    table.add_column("Frontend SPA", justify="center", style="white", width=12)
    table.add_column("Fullstack", justify="center", style="white", width=12)
    table.add_column("Static Site", justify="center", style="white", width=12)

    template_map = create_template_mapping()
    
    backend_templates = [(k, v) for k, v in template_map.items() if v in TEMPLATE_CATEGORIES.get("Backend API", []) and k.isdigit()]
    frontend_templates = [(k, v) for k, v in template_map.items() if v in TEMPLATE_CATEGORIES.get("Frontend SPA", []) and k.isdigit()]
    fullstack_templates = [(k, v) for k, v in template_map.items() if v in TEMPLATE_CATEGORIES.get("Fullstack", []) and k.isdigit()]
    static_templates = [(k, v) for k, v in template_map.items() if v in TEMPLATE_CATEGORIES.get("Static Site", []) and k.isdigit()]

    max_items = max(len(backend_templates), len(frontend_templates), len(fullstack_templates), len(static_templates))

    for i in range(max_items):
        row = []
        if i < len(backend_templates):
            row.append(f"{backend_templates[i][0]}. {backend_templates[i][1]}")
        else:
            row.append("")
        if i < len(frontend_templates):
            row.append(f"{frontend_templates[i][0]}. {frontend_templates[i][1]}")
        else:
            row.append("")
        if i < len(fullstack_templates):
            row.append(f"{fullstack_templates[i][0]}. {fullstack_templates[i][1]}")
        else:
            row.append("")
        if i < len(static_templates):
            row.append(f"{static_templates[i][0]}. {static_templates[i][1]}")
        else:
            row.append("")
        table.add_row(*row)

    console.print(table)

def show_docker_components_table():
    console = Console()
    table = Table(title=" Docker Components", show_header=True, header_style="bold white")

    table.add_column("Backend", justify="center", style="white", width=12)
    table.add_column("Frontend", justify="center", style="white", width=12)
    table.add_column("Fullstack", justify="center", style="white", width=12)
    table.add_column("Database", justify="center", style="white", width=14)
    table.add_column("Cache/Queue", justify="center", style="white", width=12)
    table.add_column("Proxy", justify="center", style="white", width=12)
    table.add_column("Monitoring", justify="center", style="white", width=14)

    max_items = max(len(components) for components in EnvFactory.DOCKER_COMPONENT_CATEGORIES.values())

    backend_components = EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Backend", [])
    frontend_components = EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Frontend", [])
    fullstack_components = EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Fullstack", [])
    database_components = EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Database", [])
    cache_queue_components = EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Cache/Queue", [])
    proxy_components = EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Proxy", [])
    monitoring_components = EnvFactory.DOCKER_COMPONENT_CATEGORIES.get("Monitoring", [])

    backend_start_id = 1
    frontend_start_id = backend_start_id + len(backend_components)
    fullstack_start_id = frontend_start_id + len(frontend_components)
    database_start_id = fullstack_start_id + len(fullstack_components)
    cache_queue_start_id = database_start_id + len(database_components)
    proxy_start_id = cache_queue_start_id + len(cache_queue_components)
    monitoring_start_id = proxy_start_id + len(proxy_components)

    for i in range(max_items):
        row = []
        if i < len(backend_components):
            row.append(f"{backend_start_id + i}. {backend_components[i]}")
        else:
            row.append("")

        if i < len(frontend_components):
            row.append(f"{frontend_start_id + i}. {frontend_components[i]}")
        else:
            row.append("")

        if i < len(fullstack_components):
            row.append(f"{fullstack_start_id + i}. {fullstack_components[i]}")
        else:
            row.append("")

        if i < len(database_components):
            row.append(f"{database_start_id + i}. {database_components[i]}")
        else:
            row.append("")

        if i < len(cache_queue_components):
            row.append(f"{cache_queue_start_id + i}. {cache_queue_components[i]}")
        else:
            row.append("")

        if i < len(proxy_components):
            row.append(f"{proxy_start_id + i}. {proxy_components[i]}")
        else:
            row.append("")

        if i < len(monitoring_components):
            row.append(f"{monitoring_start_id + i}. {monitoring_components[i]}")
        else:
            row.append("")
        table.add_row(*row)

    console.print(table)

def show_main_menu():
    table = Table(title=" Available Actions")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    table.add_row("1", " Create from pattern (brace expansion)")
    table.add_row("2", " Create from template")
    table.add_row("3", " Create Docker combo")
    table.add_row("4", " Configure settings")
    table.add_row("0", " Exit")

    console = Console()
    console.print(table)
