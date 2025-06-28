from pathlib import Path

def preview_structure(expanded_paths, indent=0):
    """
    Prints a visual tree preview of the project structure.
    """
    if not expanded_paths:
        return

    expanded_paths = sorted(list(set(expanded_paths)))

    tree = {}
    for path in expanded_paths:
        parts = Path(path).parts
        current_level = tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

    def print_tree(node, prefix=""):
        if not node:
            return
        items = sorted(node.keys())
        for i, item in enumerate(items):
            connector = "├── " if i < len(items) - 1 else "└── "
            print(f"{prefix}{connector}{item}/")
            if node[item]:
                extension = "│   " if i < len(items) - 1 else "    "
                print_tree(node[item], prefix + extension)

    print("Preview structure:")
    print_tree(tree)
