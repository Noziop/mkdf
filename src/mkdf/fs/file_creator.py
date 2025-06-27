from pathlib import Path

def create_file(path, content='', force=False):
    """Creates a file, with template handling and force option."""
    path = Path(path)
    if path.exists() and not force:
        print(f"File already exists: {path}")
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"Created file: {path}")
    except IOError as e:
        print(f"Error creating file {path}: {e}")
