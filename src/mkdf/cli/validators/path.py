import os
from pathlib import Path

def get_project_path(project_name=""):
    """Get and validate project path with proper defaults."""
    default_base = Path(os.path.expanduser("~/projects/"))
    default_base.mkdir(parents=True, exist_ok=True)

    prompt_text = "Enter Project path (absolute path) [ Default : ~/projects/ ]: "
    user_input = input(prompt_text).strip()

    if not user_input:
        final_path = default_base / project_name if project_name else default_base
    elif user_input.startswith(('~', '/')) or (':' in user_input and Path(user_input).is_absolute()):
        expanded_path = Path(os.path.expanduser(user_input))
        final_path = expanded_path / project_name if project_name else expanded_path
    else:
        final_path = default_base / user_input
        if project_name and not str(final_path).endswith(project_name):
             final_path = final_path / project_name

    return str(final_path)
