import os
from pathlib import Path

def is_file_path(path: str) -> bool:
    """
    Correctly detect if path is a file:
    - 'README.md' -> True (file)
    - 'src/' -> False (directory)
    - 'src' -> False (directory, no extension)
    """
    # A path is a directory if it ends with a slash.
    if path.endswith(os.path.sep):
        return False
    # A path is a file if the last part of the path contains a dot.
    basename = os.path.basename(path)
    if '.' in basename and basename.rfind('.') < len(basename) - 1:
        return True
    return False

def is_dir_path(path: str) -> bool:
    """
    Correctly detect directories:
    - Ends with '/' -> True
    - No extension and no '/' -> True
    - Has extension -> False
    """
    return not is_file_path(path)