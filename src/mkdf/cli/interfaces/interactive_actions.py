import os
import time
from pathlib import Path
from rich.console import Console

from ...fs.brace_expansion import brace_expand
from ...fs.path_analyzer import is_file_path
from ...fs.dir_creator import create_directory
from ...fs.file_creator import create_file
from ..ui.previews import preview_structure
from ..ui.tables import show_templates_table, show_docker_components_table
from ..validators.path import get_project_path
from ..models.ports import get_interactive_port_config
from ..models.mappings import create_template_mapping, create_component_mapping
from ...core import create_from_template

console = Console()

def interactive_create_from_pattern():
    """
    Interactive CLI interface for creating project structures from brace expansion patterns.
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
                print("\n⏳ Returning to main menu in 5 seconds...")
                time.sleep(5)
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            elif confirm == 'n':
                print("Creation cancelled. Returning to main menu.")
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        except Exception as e:
            print(f"Error processing pattern: {e}. Please try again.")

def interactive_create_from_template(banner_callback=None):
    """
    Interactive CLI interface for creating projects from predefined templates.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
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
            os.system('cls' if os.name == 'nt' else 'clear')
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
                show_docker_components_table()
                components_input = input("Enter Docker components (e.g., 1 8 14), separated by space or comma: ")
                components = []
                component_map = create_component_mapping()
                for item in components_input.replace(' ', ',').split(','):
                    item = item.strip()
                    if item in component_map:
                        components.append(component_map[item])
                    elif item.isdigit() and int(item) in range(1, len(component_map) + 1):
                        components.append(component_map[str(item)])
                
                if not components:
                    print("No valid Docker components selected. Please try again.")
                    continue

                port_config = get_interactive_port_config()

            full_project_path = get_project_path(project_name)

            try:
                confirm = input(f"Create project '{project_name}' using template '{template_type}' at {full_project_path}? (y/n): ").lower()
                if confirm == 'y':
                    create_from_template(project_name, template_type, components, base_path=str(full_project_path), port_config=port_config)
                    print("\n✨ Project created successfully! ✨")
                    print(" You can now navigate to the project directory to start coding!")
                    print("\n⏳ Returning to main menu in 7 seconds...")
                    time.sleep(7)
                    os.system('cls' if os.name == 'nt' else 'clear')
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

def interactive_create_docker_combo(banner_callback=None):
    os.system('cls' if os.name == 'nt' else 'clear')
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
        
        selected_components = []
        for item in choice.replace(' ', ',').split(','):
            item = item.strip()
            if item in component_map:
                selected_components.append(component_map[item])
            elif item.isdigit() and int(item) in range(1, len(component_map) + 1):
                selected_components.append(component_map[str(item)])
        
        if not selected_components:
            print("No valid components selected. Try again.")
            continue
            
        print(f"Selected components: {selected_components}")
        
        project_name = input("Enter project name: ").strip()
        if not project_name:
            print("Project name cannot be empty.")
            continue

        port_config = get_interactive_port_config()
            
        full_path = get_project_path(project_name)
        
        confirm = input(f"Create Docker project '{project_name}' with {selected_components} at {full_path}? (y/n): ")
        if confirm.lower() == 'y':
            try:
                create_from_template(project_name, 'docker', selected_components, base_path=str(full_path), port_config=port_config)
                print(f"Successfully created Docker project '{project_name}'!")
                print("✨ Project created successfully! ✨")
                print(" You can now navigate to the project directory to start coding!")
                print("⏳ Returning to main menu in 5 seconds...")
                time.sleep(5)
                return
            except Exception as e:
                print(f"Error creating project: {e}")
        else:
            print("Creation cancelled.")
            continue

def interactive_configure_settings(banner_callback=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    if banner_callback:
        banner_callback()

    print("\n=== ⚙️ Configuration Settings ===")
    print("1. Default project path")
    print("2. Default ports (backend/frontend)")  
    print("3. Preferred templates")
    print("0. Return to main menu")

    choice = input("\nYour choice: ").strip()
    if choice == "0":
        return
    else:
        print("Configuration coming soon!")
        input("Press Enter to continue...")
