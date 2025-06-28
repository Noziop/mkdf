import os
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from ..fs.brace_expansion import brace_expand
from ..fs.path_analyzer import is_file_path
from ..fs.dir_creator import create_directory
from ..fs.file_creator import create_file
from ..templates.template_factory import TemplateFactory, TEMPLATE_CATEGORIES
from ..config.config_manager import ConfigManager
from ..templates.factories.env_factory import EnvFactory

config_manager = ConfigManager()

def get_interactive_port_config():
    """Interactive port configuration"""
    print("\n=== Port Configuration (press Enter for defaults) ===")
    backend_port = input("Backend port [8000]: ").strip() or "8000"
    frontend_port = input("Frontend port [3000]: ").strip() or "3000"
    subnet = input("Docker subnet [172.18.0.0/16]: ").strip() or "172.18.0.0/16"
    prometheus_port = input("Prometheus port [9090]: ").strip() or "9090"
    grafana_port = input("Grafana port [3001]: ").strip() or "3001"
    traefik_port = input("Traefik HTTP port [80]: ").strip() or "80"
    traefik_dashboard_port = input("Traefik dashboard port [8080]: ").strip() or "8080"

    return {
        'backend': int(backend_port),
        'frontend': int(frontend_port),
        'subnet': subnet,
        'prometheus': int(prometheus_port),
        'grafana': int(grafana_port),
        'traefik': int(traefik_port),
        'traefik_dashboard': int(traefik_dashboard_port),
    }

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_project_path(project_name=""):
    """Get and validate project path with proper defaults."""
    # Ensure the default base directory exists
    default_base = Path(os.path.expanduser("~/projects/"))
    default_base.mkdir(parents=True, exist_ok=True)

    prompt_text = "Enter Project path (absolute path) [ Default : ~/projects/ ]: "
    user_input = input(prompt_text).strip()

    if not user_input:
        # Case 1: No input -> use the default path
        final_path = default_base / project_name if project_name else default_base
    elif user_input.startswith(('~', '/')) or (':' in user_input and Path(user_input).is_absolute()):
        # Case 2: Absolute path -> expand it
        expanded_path = Path(os.path.expanduser(user_input))
        final_path = expanded_path / project_name if project_name else expanded_path
    else:
        # Case 3: Relative path -> relative to the default base
        final_path = default_base / user_input
        if project_name and not str(final_path).endswith(project_name):
             final_path = final_path / project_name

    return str(final_path)

def _create_from_template_recursive(base_path, template_dict):
    """
    Recursively creates directories and files from a template dictionary.
    
    Args:
        base_path (str): The base directory path where files/directories will be created
        template_dict (dict): Dictionary representing the directory structure and file contents
                             where keys are names and values are either dicts (for directories) 
                             or strings (for file contents)
    """
    for name, content in template_dict.items():
        current_path = os.path.join(base_path, name)
        if isinstance(content, dict):
            create_directory(current_path)
            _create_from_template_recursive(current_path, content)
        elif content is None:
            create_directory(current_path)
        else:
            create_file(current_path, str(content))

def preview_structure(expanded_paths, indent=0):
    """
    Prints a visual tree preview of the project structure.
    
    Args:
        expanded_paths (list): List of paths to be visualized in the tree structure
        indent (int, optional): Initial indentation level. Defaults to 0.
    """
    if not expanded_paths:
        return

    # Sort paths to ensure consistent tree display
    expanded_paths = sorted(list(set(expanded_paths)))

    # Build a tree-like dictionary
    tree = {}
    for path in expanded_paths:
        parts = Path(path).parts
        current_level = tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

    def print_tree(node, prefix=""):
        if not node:
            return
        items = sorted(node.keys())
        for i, item in enumerate(items):
            connector = "├── " if i < len(items) - 1 else "└── "
            print(f"{prefix}{connector}{item}/")
            if node[item]:
                extension = "│   " if i < len(items) - 1 else "    "
                print_tree(node[item], prefix + extension)

    print("Preview structure:")
    print_tree(tree)

def interactive_create_from_pattern():
    """
    Interactive CLI interface for creating project structures from brace expansion patterns.
    
    This function prompts the user for a pattern using brace expansion syntax,
    displays a preview of the resulting structure, and creates the directories and files
    if confirmed by the user.
    """
    while True:
        pattern = input("Enter pattern (e.g., 'project/{src/,docs/,tests/}'): ")
        try:
            expanded_paths = brace_expand(pattern)
            if not expanded_paths:
                print("No paths generated from the pattern. Please try again.")
                continue

            preview_structure(expanded_paths)

            confirm = input("Create this structure? (y/n): ").lower()
            if confirm == 'y':
                project_path = get_project_path()
                Path(project_path).mkdir(parents=True, exist_ok=True)

                for path in expanded_paths:
                    full_path = Path(project_path) / path
                    if is_file_path(str(full_path)):
                        create_file(str(full_path))
                    else:
                        create_directory(str(full_path))
                print("Project structure created successfully!")
                print("\n✨ Project created successfully! ✨")
                print(" You can now navigate to the project directory to start coding!")
                print("\n⏳ Returning to main menu in 7 seconds...")
                time.sleep(7)
                clear_screen()
                break
            elif confirm == 'n':
                print("Creation cancelled. Returning to main menu.")
                clear_screen()
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        except Exception as e:
            print(f"Error processing pattern: {e}. Please try again.")

def show_templates_table():
    console = Console()

    table = Table(title=" Project Templates", show_header=True, header_style="bold magenta")

    # Neutral columns (no colors)
    table.add_column("Backend API", justify="center", style="white", width=12)
    table.add_column("Frontend SPA", justify="center", style="white", width=12)
    table.add_column("Fullstack", justify="center", style="white", width=10)
    table.add_column("Static", justify="center", style="white", width=8)

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

def create_template_mapping():
    template_map = {}
    i = 1
    for category, templates in TEMPLATE_CATEGORIES.items():
        for template in templates:
            template_map[str(i)] = template
            template_map[template] = template
            i += 1
    return template_map

def interactive_create_from_template(banner_callback=None):
    """
    Interactive CLI interface for creating projects from predefined templates.
    
    This function displays available templates, prompts the user to select one,
    collects necessary project information, and creates the project structure
    based on the selected template.
    """
    clear_screen()
    if banner_callback:
        banner_callback()
    
    print("\n===  Template Creator ===")

    while True:
        show_templates_table()
        template_map = create_template_mapping()
        
        print("\n Selection Options:")
        print("-  By numbers: 1,5,13 (sequential IDs)")
        print("-  By names: fastapi,vue,simple") 
        print("-  Mixed: 1,vue,static")
        print("\n0. Return to main menu")
        
        choice = input("Enter template number or name: ")
        template_type = None
        if choice == '0':
            print("Returning to main menu.")
            clear_screen()
            return
        
        if choice in template_map:
            template_type = template_map[choice]

        if template_type:
            project_name = input("Enter project name: ")
            if not project_name:
                print("Project name cannot be empty.")
                continue
                
            components = None
            port_config = None
            if template_type == 'docker':
                print("Available Docker Components:")
                for comp_name in EnvFactory.DOCKER_COMPONENT_CATEGORIES.keys():
                    print(f"- {comp_name}")
                components_input = input("Enter Docker components (e.g., fastapi vue monitoring), separated by space: ")
                components = components_input.split()
                port_config = get_interactive_port_config()

            full_project_path = get_project_path(project_name)

            try:
                # template = factory.create_template(template_type, components)
                # Preview for templates is more complex, so we'll skip for now or provide a simpler one
                confirm = input(f"Create project '{project_name}' using template '{template_type}' at {full_project_path}? (y/n): ").lower()
                if confirm == 'y':
                    from ..core import create_from_template
                    create_from_template(project_name, template_type, components, base_path=str(full_project_path), port_config=port_config)
                    print("\n✨ Project created successfully! ✨")
                    print(" You can now navigate to the project directory to start coding!")
                    print("\n⏳ Returning to main menu in 7 seconds...")
                    time.sleep(7)
                    clear_screen()
                    break
                elif confirm == 'n':
                    print("Creation cancelled. Returning to template selection.")
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print("Invalid template selection. Please try again.")

def start_interactive_mode(banner_callback=None):
    """
    Starts the MKDF interactive command-line interface.
    
    This function presents the main menu for the interactive mode and 
    handles navigation between different functionality options.
    """
    while True:
        clear_screen()
        if banner_callback:
            banner_callback()
        print("=== MKDF Interactive Mode ===")
        print("Choose an option:")
        print("1. Create from pattern (brace expansion)")
        print("2. Create from template")
        print("3. Create Docker combo")
        print("4. Configure settings")
        print("5. Exit")

        choice = input("Your choice: ")

        if choice == '1':
            interactive_create_from_pattern()
        elif choice == '2':
            interactive_create_from_template(banner_callback)
        elif choice == '3':
            interactive_create_docker_combo(banner_callback)
        elif choice == '4':
            interactive_configure_settings(banner_callback)
        elif choice == '5':
            print("Exiting MKDF Interactive Mode. Goodbye!")
            break

def interactive_configure_settings(banner_callback=None):
    clear_screen()
    if banner_callback:
        banner_callback()

    print("\n=== ⚙️ Configuration Settings ===")
    print("1. Default project path")
    print("2. Default ports (backend/frontend)")  
    print("3. Preferred templates")
    print("0. Return to main menu")

    # Basic implementation for now
    choice = input("\nYour choice: ").strip()
    if choice == "0":
        return
    else:
        print("Configuration coming soon!")
        input("Press Enter to continue...")

def get_port_configuration():
    """Interactive port configuration"""
    print("=== Port Configuration ===")
    print("Press Enter to use default ports, or specify custom ports:")

    backend_port = input("Backend port [8000]: ").strip() or "8000"
    frontend_port = input("Frontend port [3000]: ").strip() or "3000"
    subnet = input("Docker subnet [172.18.0.0/16]: ").strip() or "172.18.0.0/16"

    return {
        'backend': int(backend_port),
        'frontend': int(frontend_port),
        'subnet': subnet,
        'database': 5432,  # Default, will be auto-detected later
        'redis': 6379,
        'prometheus': 9090,
        'grafana': 3001,
        'traefik': 80,
        'traefik_dashboard': 8080,
    }

def show_docker_components_table():
    console = Console()
    table = Table(title=" Docker Components", show_header=True, header_style="bold magenta")

    # Add columns for each category
    table.add_column("Backend", justify="center", style="white", width=10)
    table.add_column("Frontend", justify="center", style="white", width=10)
    table.add_column("Fullstack", justify="center", style="white", width=10)
    table.add_column("Database", justify="center", style="white", width=10)
    table.add_column("Cache/Queue", justify="center", style="white", width=12)
    table.add_column("Proxy", justify="center", style="white", width=8)
    table.add_column("Monitoring", justify="center", style="white", width=12)

    # Create rows by filling each category column
    max_items = max(len(components) for components in EnvFactory.DOCKER_COMPONENT_CATEGORIES.values())

    for i in range(max_items):
        row = []
        for category, components in EnvFactory.DOCKER_COMPONENT_CATEGORIES.items():
            if i < len(components):
                row.append(components[i])
            else:
                row.append("")
        table.add_row(*row)

    console.print(table)

def create_component_mapping():
    """Create mapping for sequential numbers and component names"""
    components_flat = []
    for category, components in EnvFactory.DOCKER_COMPONENT_CATEGORIES.items():
        components_flat.extend(components)

    component_map = {}
    for i, component in enumerate(components_flat, 1):
        component_map[str(i)] = component
        component_map[component] = component  # Allow name selection

    return component_map

def interactive_create_docker_combo(banner_callback=None):
    clear_screen()
    if banner_callback:
        banner_callback()
    
    print("\n===  Docker Combo Creator ===")

    while True:
        show_docker_components_table()
        component_map = create_component_mapping()
        
        print("\n Selection Options:")
        print("-  By numbers: 1,5,13 (sequential IDs)")
        print("-  By names: fastapi,vue,postgresql")
        print("-  Mixed: 1,vue,redis")
        print("\n0. Return to main menu")
        
        choice = input("\nYour choice: ").strip()
        
        if choice == '0':
            return
        
        # Parse selection
        selected_components = []
        for item in choice.split(','):
            item = item.strip()
            if item in component_map:
                selected_components.append(component_map[item])
        
        if not selected_components:
            print("No valid components selected. Try again.")
            continue
            
        print(f"Selected components: {selected_components}")
        
        project_name = input("Enter project name: ").strip()
        if not project_name:
            print("Project name cannot be empty.")
            continue

        port_config = get_port_configuration()
            
        full_path = get_project_path(project_name)
        
        confirm = input(f"Create Docker project '{project_name}' with {selected_components} at {full_path}? (y/n): ")
        if confirm.lower() == 'y':
            try:
                from ..core import create_from_template
                create_from_template(project_name, 'docker', selected_components, base_path=str(full_path), port_config=port_config)
                print(f"Successfully created Docker project '{project_name}'!")
                print("✨ Project created successfully! ✨")
                print(" You can now navigate to the project directory to start coding!")
                print("⏳ Returning to main menu in 7 seconds...")
                time.sleep(7)
                return
            except Exception as e:
                print(f"Error creating project: {e}")
        else:
            print("Creation cancelled.")
            continue

def create_project_structure(structure, base_path):
    """
    Creates the project file and directory structure based on a template dictionary.
    
    Args:
        structure (dict): Dictionary representing the directory structure and file contents
                          where keys are names and values are either dicts (for directories) 
                          or strings (for file contents)
        base_path (str): The root directory path where the project structure will be created
    """
    from ..fs.dir_creator import create_directory
    from ..fs.file_creator import create_file
    
    def create_recursive(items, current_path):
        for name, content in items.items():
            item_path = os.path.join(current_path, name)
            
            if isinstance(content, dict):
                # C'est un répertoire
                create_directory(item_path)
                create_recursive(content, item_path)
            else:
                # C'est un fichier
                create_file(item_path, content)
    
    # Créer le répertoire racine
    create_directory(base_path)
    # Créer la structure récursivement
    create_recursive(structure, base_path)

