import os
import time
from ..ui.banner import show_rainbow_banner
from ..ui.tables import show_main_menu
from .interactive_actions import (
    interactive_create_from_pattern,
    interactive_create_from_template,
    interactive_create_docker_combo,
    interactive_configure_settings
)

def start_interactive_mode(banner_callback=None):
    """
    Starts the MKDF interactive command-line interface.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if banner_callback:
            banner_callback()
        
        show_main_menu()

        choice = input("Your choice: ")

        if choice == '1':
            interactive_create_from_pattern()
        elif choice == '2':
            interactive_create_from_template(banner_callback)
        elif choice == '3':
            interactive_create_docker_combo(banner_callback)
        elif choice == '4':
            interactive_configure_settings(banner_callback)
        elif choice == '0':
            print("Exiting MKDF Interactive Mode. Thank you for using MKDF! Goodbye!")
            break
