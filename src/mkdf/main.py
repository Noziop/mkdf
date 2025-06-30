from .cli.parsers.main_parser import app
from .cli.commands.web import web

app.add_typer(web, name="web")

def main():
    app()

if __name__ == '__main__':
    main()
