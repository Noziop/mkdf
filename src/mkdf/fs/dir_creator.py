from pathlib import Path

def create_directory(path, force=False):
    """Creates a directory, with recursive creation and force option."""
    path = Path(path)
    if path.exists() and not force:
        print(f"Directory already exists: {path}")
        return
    try:
        path.mkdir(parents=True, exist_ok=force)
        print(f"Created directory: {path}")
    except OSError as e:
        print(f"Error creating directory {path}: {e}")
