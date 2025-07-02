from pathlib import Path
import os

def _to_pathlib_path(path_str: str) -> Path:
    """Converts a string path to a pathlib.Path object, expanding user tilde."""
    return Path(os.path.expanduser(path_str))

def expand_tilde(path): # Keeping this for backward compatibility for now
    """Expands the tilde (~) in a path to the user's home directory."""
    return Path(path).expanduser()

def is_path_safe(path: str) -> bool:
    """Checks if a given path is safe to use, avoiding system directories."""
    forbidden = ["/etc", "/bin", "/usr", "/var", "/root", "/sys", "/proc", "/dev", "/boot", "/lib", "/sbin"]
    abs_path = os.path.abspath(path)
    return not any(abs_path.startswith(f) for f in forbidden)