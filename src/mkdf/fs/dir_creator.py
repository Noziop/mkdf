import shutil
from pathlib import Path
from .fs_utils import _to_pathlib_path, is_path_safe

def create_directory(path: str | Path, overwrite: bool = True):
    """Creates a directory, with recursive creation.

    Args:
        path: The path to the directory to create.
        overwrite: If True, remove existing directory and recreate it. If False, raise FileExistsError if the directory exists.

    Raises:
        FileExistsError: If the directory already exists and overwrite is False.
        OSError: For other operating system related errors during directory creation.
    """
    if not is_path_safe(path):
        raise ValueError(f"Unsafe path detected: {path}. Please choose a different path.")
    path_obj = _to_pathlib_path(str(path))
    try:
        if path_obj.exists():
            if overwrite:
                shutil.rmtree(path_obj) # Remove existing directory to truly overwrite
            else:
                raise FileExistsError(f"Directory already exists: {path_obj}")
        path_obj.mkdir(parents=True) # Create the directory (now it's guaranteed not to exist or was just removed)
    except OSError as e:
        raise OSError(f"Error creating directory {path_obj}: {e}") from e
