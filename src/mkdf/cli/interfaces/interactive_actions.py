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

            project_path = get_project_path()
            full_project_path = os.path.join(project_path, project_name)

            try:
                confirm = input(f"Create project '{project_name}' using template '{template_type}' at {full_project_path}? (y/n): ").lower()
                if confirm == 'y':
                    create_from_template(project_name, template_type, components, base_path=project_path, port_config=port_config)
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
            
        project_path = get_project_path()
        full_path = os.path.join(project_path, project_name)
        
        confirm = input(f"Create Docker project '{project_name}' with {selected_components} at {full_path}? (y/n): ")
        if confirm.lower() == 'y':
            try:
                create_from_template(project_name, 'docker', selected_components, base_path=project_path, port_config=port_config)
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

from ...config.config_manager import ConfigManager, CONFIG_FILE
import json

config_manager = ConfigManager()

def interactive_configure_settings(banner_callback=None):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if banner_callback:
            banner_callback()

        print("\n=== ⚙️ Configuration Settings ===")
        print("1. View current configuration")
        print("2. Set Default project path")
        print("3. Set Web server port")
        print("4. Set Preferred templates")
        print("5. Set Author name/email")
        print("6. Toggle Debug mode")
        print("7. Template directory paths (read-only)")
        print("8. Export configuration")
        print("9. Import configuration")
        print("0. Return to main menu")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            view_current_configuration()
        elif choice == "2":
            set_default_project_path()
        elif choice == "3":
            set_web_server_port()
        elif choice == "4":
            set_preferred_templates()
        elif choice == "5":
            set_author_info()
        elif choice == "6":
            toggle_debug_mode()
        elif choice == "7":
            view_template_directory_paths()
        elif choice == "8":
            export_configuration()
        elif choice == "9":
            import_configuration()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please try again.")
        input("Press Enter to continue...")

def view_current_configuration():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Current Configuration ===")
    for key, value in config_manager.config.items():
        print(f"{key}: {value}")

def set_default_project_path():
    current_path = config_manager.get("default_project_path")
    new_path = input(f"Enter new default project path (current: {current_path}): ").strip()
    if new_path:
        try:
            Path(new_path).mkdir(parents=True, exist_ok=True)
            config_manager.set("default_project_path", new_path)
            print(f"Default project path set to: {new_path}")
        except Exception as e:
            print(f"Error setting path: {e}")
    else:
        print("Path not changed.")

def set_web_server_port():
    current_port = config_manager.get("web_port_start")
    new_port_str = input(f"Enter new web server port (current: {current_port}): ").strip()
    if new_port_str:
        try:
            new_port = int(new_port_str)
            if 1024 <= new_port <= 65535:
                config_manager.set("web_port_start", new_port)
                print(f"Web server port set to: {new_port}")
            else:
                print("Invalid port number. Must be between 1024 and 65535.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("Port not changed.")

from ...templates.template_factory import TEMPLATE_CATEGORIES
from ...templates.factories.env_factory import EnvFactory

def set_preferred_templates():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Set Preferred Templates ===")
    show_templates_table()
    template_map = create_template_mapping()

    current_backend = config_manager.get("preferred_templates", {}).get("backend", "N/A")
    print(f"Current Backend: {current_backend}")
    backend_choice = input("Enter preferred backend template (name or number, leave empty to keep current): ").strip()
    if backend_choice:
        selected_backend = template_map.get(backend_choice)
        if selected_backend and selected_backend in TEMPLATE_CATEGORIES.get("Backend API", []):
            config_manager.config["preferred_templates"]["backend"] = selected_backend
            config_manager.set("preferred_templates", config_manager.config["preferred_templates"])
            print(f"Preferred backend set to: {selected_backend}")
        else:
            print("Invalid backend template. Keeping current.")

    current_frontend = config_manager.get("preferred_templates", {}).get("frontend", "N/A")
    print(f"Current Frontend: {current_frontend}")
    frontend_choice = input("Enter preferred frontend template (name or number, leave empty to keep current): ").strip()
    if frontend_choice:
        selected_frontend = template_map.get(frontend_choice)
        if selected_frontend and selected_frontend in TEMPLATE_CATEGORIES.get("Frontend SPA", []):
            config_manager.config["preferred_templates"]["frontend"] = selected_frontend
            config_manager.set("preferred_templates", config_manager.config["preferred_templates"])
            print(f"Preferred frontend set to: {selected_frontend}")
        else:
            print("Invalid frontend template. Keeping current.")

    current_fullstack = config_manager.get("preferred_templates", {}).get("fullstack", "N/A")
    print(f"Current Fullstack: {current_fullstack}")
    fullstack_choice = input("Enter preferred fullstack template (name or number, leave empty to keep current): ").strip()
    if fullstack_choice:
        selected_fullstack = template_map.get(fullstack_choice)
        if selected_fullstack and selected_fullstack in TEMPLATE_CATEGORIES.get("Fullstack", []):
            config_manager.config["preferred_templates"]["fullstack"] = selected_fullstack
            config_manager.set("preferred_templates", config_manager.config["preferred_templates"])
            print(f"Preferred fullstack set to: {selected_fullstack}")
        else:
            print("Invalid fullstack template. Keeping current.")

def set_preferred_docker_combo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Set Preferred Docker Combo ===")
    show_docker_components_table()
    component_map = create_component_mapping()

    current_combo = config_manager.get("preferred_docker_combo", "N/A")
    print(f"Current Preferred Docker Combo: {current_combo}")

    components_input = input("Enter Docker components (space-separated names or numbers, leave empty to keep current): ").strip()
    if components_input:
        selected_components = []
        for item in components_input.replace(' ', ',').split(','):
            item = item.strip()
            if item in component_map:
                selected_components.append(component_map[item])
            elif item.isdigit() and int(item) in range(1, len(component_map) + 1):
                selected_components.append(component_map[str(item)])
        
        if selected_components:
            config_manager.set("preferred_docker_combo", " ".join(selected_components))
            print(f"Preferred Docker combo set to: {' '.join(selected_components)}")
        else:
            print("No valid components selected. Keeping current combo.")
    else:
        print("Docker combo not changed.")

def interactive_configure_settings(banner_callback=None):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if banner_callback:
            banner_callback()

        print("\n=== ⚙️ Configuration Settings ===")
        print("1. View current configuration")
        print("2. Set Default project path")
        print("3. Set Web server port")
        print("4. Set Preferred templates")
        print("5. Set Preferred Docker combo")
        print("6. Set Author name/email")
        print("7. Toggle Debug mode")
        print("8. Template directory paths (read-only)")
        print("9. Export configuration")
        print("10. Import configuration")
        print("0. Return to main menu")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            view_current_configuration()
        elif choice == "2":
            set_default_project_path()
        elif choice == "3":
            set_web_server_port()
        elif choice == "4":
            set_preferred_templates()
        elif choice == "5":
            set_preferred_docker_combo()
        elif choice == "6":
            set_author_info()
        elif choice == "7":
            toggle_debug_mode()
        elif choice == "8":
            view_template_directory_paths()
        elif choice == "9":
            export_configuration()
        elif choice == "10":
            import_configuration()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please try again.")
        input("Press Enter to continue...")

def view_current_configuration():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Current Configuration ===")
    for key, value in config_manager.config.items():
        print(f"{key}: {value}")

def set_default_project_path():
    current_path = config_manager.get("default_project_path")
    new_path = input(f"Enter new default project path (current: {current_path}): ").strip()
    if new_path:
        try:
            Path(new_path).mkdir(parents=True, exist_ok=True)
            config_manager.set("default_project_path", new_path)
            print(f"Default project path set to: {new_path}")
        except Exception as e:
            print(f"Error setting path: {e}")
    else:
        print("Path not changed.")

def set_web_server_port():
    current_port = config_manager.get("web_port_start")
    new_port_str = input(f"Enter new web server port (current: {current_port}): ").strip()
    if new_port_str:
        try:
            new_port = int(new_port_str)
            if 1024 <= new_port <= 65535:
                config_manager.set("web_port_start", new_port)
                print(f"Web server port set to: {new_port}")
            else:
                print("Invalid port number. Must be between 1024 and 65535.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("Port not changed.")

def set_author_info():
    current_name = config_manager.get("author_name")
    current_email = config_manager.get("author_email")

    new_name = input(f"Enter author name (current: {current_name}): ").strip()
    if new_name:
        config_manager.set("author_name", new_name)
        print(f"Author name set to: {new_name}")

    new_email = input(f"Enter author email (current: {current_email}): ").strip()
    if new_email:
        config_manager.set("author_email", new_email)
        print(f"Author email set to: {new_email}")

def toggle_debug_mode():
    current_logging_enabled = config_manager.get("enable_logging")
    current_log_level = config_manager.get("log_level")

    print(f"Current logging enabled: {current_logging_enabled}")
    print(f"Current log level: {current_log_level}")

    toggle_choice = input("Toggle logging (y/n, current: {})".format('y' if current_logging_enabled else 'n')).strip().lower()
    if toggle_choice == 'y':
        config_manager.set("enable_logging", True)
        print("Logging enabled.")
    elif toggle_choice == 'n':
        config_manager.set("enable_logging", False)
        print("Logging disabled.")
    else:
        print("No change to logging status.")

    if config_manager.get("enable_logging"):
        new_log_level = input(f"Set log level (INFO, DEBUG, WARNING, ERROR, CRITICAL, current: {current_log_level}): ").strip().upper()
        if new_log_level in ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]:
            config_manager.set("log_level", new_log_level)
            print(f"Log level set to: {new_log_level}")
        else:
            print("Invalid log level. No change.")

def view_template_directory_paths():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Template Directory Paths ===")
    print(f"Templates Directory: {config_manager.get('templates_dir')}")
    print("\nNote: This setting is read-only and cannot be changed directly from here.")

def export_configuration():
    export_path_str = input(f"Enter path to export configuration (default: {CONFIG_FILE}.bak): ").strip()
    if not export_path_str:
        export_path = Path(str(CONFIG_FILE) + ".bak")
    else:
        export_path = Path(export_path_str)

    try:
        with open(export_path, 'w') as f:
            json.dump(config_manager.config, f, indent=4)
        print(f"Configuration exported to: {export_path}")
    except Exception as e:
        print(f"Error exporting configuration: {e}")

def import_configuration():
    import_path_str = input("Enter path to import configuration from: ").strip()
    if not import_path_str:
        print("No path entered. Import cancelled.")
        return

    import_path = Path(import_path_str)
    if not import_path.exists():
        print("File not found.")
        return

    try:
        with open(import_path, 'r') as f:
            imported_config = json.load(f)
        
        # Validate imported config structure if necessary
        config_manager.config.update(imported_config)
        config_manager._save_user_config() # Force save the updated config
        print(f"Configuration imported from: {import_path}")
    except json.JSONDecodeError:
        print("Invalid JSON file.")
    except Exception as e:
        print(f"Error importing configuration: {e}")

def set_author_info():
    current_name = config_manager.get("author_name")
    current_email = config_manager.get("author_email")

    new_name = input(f"Enter author name (current: {current_name}): ").strip()
    if new_name:
        config_manager.set("author_name", new_name)
        print(f"Author name set to: {new_name}")

    new_email = input(f"Enter author email (current: {current_email}): ").strip()
    if new_email:
        config_manager.set("author_email", new_email)
        print(f"Author email set to: {new_email}")

def toggle_debug_mode():
    current_logging_enabled = config_manager.get("enable_logging")
    current_log_level = config_manager.get("log_level")

    print(f"Current logging enabled: {current_logging_enabled}")
    print(f"Current log level: {current_log_level}")

    toggle_choice = input("Toggle logging (y/n, current: {})".format('y' if current_logging_enabled else 'n')).strip().lower()
    if toggle_choice == 'y':
        config_manager.set("enable_logging", True)
        print("Logging enabled.")
    elif toggle_choice == 'n':
        config_manager.set("enable_logging", False)
        print("Logging disabled.")
    else:
        print("No change to logging status.")

    if config_manager.get("enable_logging"):
        new_log_level = input(f"Set log level (INFO, DEBUG, WARNING, ERROR, CRITICAL, current: {current_log_level}): ").strip().upper()
        if new_log_level in ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]:
            config_manager.set("log_level", new_log_level)
            print(f"Log level set to: {new_log_level}")
        else:
            print("Invalid log level. No change.")

def view_template_directory_paths():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Template Directory Paths ===")
    print(f"Templates Directory: {config_manager.get('templates_dir')}")
    print("\nNote: This setting is read-only and cannot be changed directly from here.")

def export_configuration():
    export_path_str = input(f"Enter path to export configuration (default: {CONFIG_FILE}.bak): ").strip()
    if not export_path_str:
        export_path = Path(str(CONFIG_FILE) + ".bak")
    else:
        export_path = Path(export_path_str)

    try:
        with open(export_path, 'w') as f:
            json.dump(config_manager.config, f, indent=4)
        print(f"Configuration exported to: {export_path}")
    except Exception as e:
        print(f"Error exporting configuration: {e}")

def import_configuration():
    import_path_str = input("Enter path to import configuration from: ").strip()
    if not import_path_str:
        print("No path entered. Import cancelled.")
        return

    import_path = Path(import_path_str)
    if not import_path.exists():
        print("File not found.")
        return

    try:
        with open(import_path, 'r') as f:
            imported_config = json.load(f)
        
        # Validate imported config structure if necessary
        config_manager.config.update(imported_config)
        config_manager._save_user_config() # Force save the updated config
        print(f"Configuration imported from: {import_path}")
    except json.JSONDecodeError:
        print("Invalid JSON file.")
    except Exception as e:
        print(f"Error importing configuration: {e}")
