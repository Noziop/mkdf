import sys
from .cli.parsers.main_parser import app
from .cli.commands.web import web

app.add_typer(web, name="web")

def is_brace_pattern(arg):
    return "{" in arg and "}" in arg

def is_path(arg):
    # On considère tout ce qui ressemble à un chemin comme un path (pas une commande)
    return "/" in arg or "." in arg

def main():
    # On récupère les arguments non optionnels
    args = [a for a in sys.argv[1:] if not a.startswith("-")]

    # Si aucun argument, laisse Typer router (mode interactif ou sous-commandes)
    if not args:
        app()
        return

    # Si pattern détecté, on gère AVANT Typer
    if any(is_brace_pattern(a) for a in args):
        from .core import create_from_pattern
        from .fs.file_creator import create_file
        from .fs.dir_creator import create_directory
        from .fs.path_analyzer import is_file_path
        for arg in args:
            if is_brace_pattern(arg):
                create_from_pattern(arg)
            else:
                if is_file_path(arg):
                    create_file(arg)
                else:
                    create_directory(arg)
        sys.exit(0)

    # Si argument ressemble à un chemin (mais pas une commande connue), on crée le fichier/dossier
    known_commands = {"create", "interactive", "web", "help"}
    if all(is_path(a) for a in args) and args[0] not in known_commands:
        from .fs.file_creator import create_file
        from .fs.dir_creator import create_directory
        from .fs.path_analyzer import is_file_path
        for arg in args:
            if is_file_path(arg):
                create_file(arg)
            else:
                create_directory(arg)
        sys.exit(0)

    # Sinon, laisse Typer router normalement (create, interactive, etc.)
    app()

if __name__ == '__main__':
    main()
