import os
from pathlib import Path
from rich.console import Console

def show_rainbow_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    console = Console()

    banner_file = Path(__file__).parent.parent / "banner.txt"

    try:
        with open(banner_file, 'r', encoding='utf-8') as f:
            ascii_lines = [line.rstrip() for line in f.readlines()]
    except FileNotFoundError:
        ascii_lines = ["MKDF - File not found"]

    pride_colors = ["red", "orange3", "yellow", "green", "blue", "purple"]

    for i, line in enumerate(ascii_lines):
        if line.strip():
            color = pride_colors[i % len(pride_colors)]
            console.print(line, style=f"bold {color}")

    print()
    console.print("━" * 90, style="bright_blue")
    console.print("️‍ Make Directories and Files - Professional Project Creator - By github.com/Noziop", style="dim")
    console.print("━" * 90, style="bright_blue")
