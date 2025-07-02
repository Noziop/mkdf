import sys
import os
from .cli.parsers.main_parser import app
from .cli.commands.web import web
from .cli.ui.panels import print_success_confirmation

app.add_typer(web, name="web", help="Launch the web interface for MKDF")

def is_brace_pattern(arg):
    return "{" in arg and "}" in arg

def is_path(arg):
    # On considère tout ce qui ressemble à un chemin comme un path (pas une commande)
    return "/" in arg or "." in arg

def main():
    """Main entry point for the mkdf CLI application."""
    args = [a for a in sys.argv[1:] if not a.startswith("-")]

    if not args:
        app()
        return

    def try_create(arg):
        from .fs.file_creator import create_file
        from .fs.dir_creator import create_directory
        from .fs.path_analyzer import is_file_path
        try:
            if is_file_path(arg):
                create_file(arg)
            else:
                create_directory(arg)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to create '{arg}': {e}")
            return False

    # Pattern mode
    if any(is_brace_pattern(a) for a in args):
        from .core import create_from_pattern
        success = True
        for arg in args:
            if is_brace_pattern(arg):
                try:
                    create_from_pattern(arg)
                except Exception as e:
                    print(f"[ERROR] Failed to create pattern '{arg}': {e}")
                    success = False
            else:
                if not try_create(arg):
                    success = False
        if success:
            project_name = "file structure"
            project_path = os.path.abspath(args[0].split("/")[0]) if args else os.getcwd()
            print_success_confirmation(project_name, project_path, template_type="custom")
        sys.exit(0)

    # Simple path mode
    known_commands = {"create", "interactive", "web", "help"}
    if all(is_path(a) for a in args) and args[0] not in known_commands:
        success = True
        for arg in args:
            if not try_create(arg):
                success = False
        if success:
            project_name = "file structure"
            project_path = os.path.abspath(args[0].split("/")[0]) if args else os.getcwd()
            print_success_confirmation(project_name, project_path, template_type="custom")
        sys.exit(0)

    app()

if __name__ == '__main__':
    main()
