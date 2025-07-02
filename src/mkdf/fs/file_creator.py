from pathlib import Path
from .fs_utils import _to_pathlib_path, is_path_safe
from .dir_creator import create_directory

def create_file(path: str | Path, content: str = '', overwrite: bool = True):
    """Creates a file.

    Args:
        path: The path to the file to create.
        content: The content to write to the file.
        overwrite: If True, overwrite existing file. If False and file exists, raises FileExistsError.

    Raises:
        FileExistsError: If the file already exists and overwrite is False.
        IOError: For other input/output related errors during file creation.
    """
    if not is_path_safe(path):
        raise ValueError(f"Unsafe path detected: {path}. Please choose a different path.")
    path_obj = _to_pathlib_path(str(path))
    try:
        if path_obj.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {path_obj}")
        path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent directory exists, don't fail if it exists
        path_obj.write_text(content)
    except IOError as e:
        raise IOError(f"Error creating file {path_obj}: {e}") from e
