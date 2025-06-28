from ..interfaces.interactive_mode import start_interactive_mode
from ..ui.banner import show_rainbow_banner

def interactive_command():
    start_interactive_mode(banner_callback=show_rainbow_banner)
