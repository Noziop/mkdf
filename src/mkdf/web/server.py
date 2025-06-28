from flask import Flask, render_template, request, jsonify, send_file
import shutil
import socket
from pathlib import Path
import os

from ..fs.dir_creator import create_directory
from ..fs.file_creator import create_file
from ..fs.brace_expansion import brace_expand
from ..fs.path_analyzer import is_file_path
from ..templates.template_factory import TemplateFactory
from mkdf.templates.factories.env_factory import EnvFactory

from ..config.config_manager import ConfigManager

app = Flask(__name__, template_folder='templates')
config_manager = ConfigManager()

@app.route('/api/docker_components')
def get_docker_components():
    return jsonify(EnvFactory.DOCKER_COMPONENT_CATEGORIES)

def find_free_port(start_port=9500, max_attempts=100):
    """Find the first available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except socket.error:
            continue
    raise RuntimeError(f"No free port found in range {start_port}-{start_port + max_attempts}")



def _generate_tree_string(expanded_paths):
    """
    Generates a visual tree string from a list of paths.
    """
    if not expanded_paths:
        return ""

    # Sort paths to ensure consistent tree display
    expanded_paths = sorted(list(set(expanded_paths)))

    # Build a tree-like dictionary
    tree = {}
    for path in expanded_paths:
        parts = Path(path).parts
        current_level = tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

    output = []
    def print_tree_recursive(node, prefix=""):
        if not node:
            return
        items = sorted(node.keys())
        for i, item in enumerate(items):
            connector = "├── " if i < len(items) - 1 else "└── "
            output.append(f"{prefix}{connector}{item}/")
            if node[item]:
                extension = "│   " if i < len(items) - 1 else "    "
                print_tree_recursive(node[item], prefix + extension)

    print_tree_recursive(tree)
    return "\n".join(output)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview_pattern', methods=['POST'])
def preview_pattern():
    data = request.get_json()
    pattern = data.get('pattern', '')
    try:
        expanded_paths = brace_expand(pattern)
        tree_string = _generate_tree_string(expanded_paths)
        return jsonify({"success": True, "tree": tree_string})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/create_pattern', methods=['POST'])
def create_pattern_web():
    data = request.get_json()
    pattern = data.get('pattern', '')
    try:
        expanded_paths = brace_expand(pattern)
        for path in expanded_paths:
            if is_file_path(path):
                create_file(path)
            else:
                create_directory(path)
        return jsonify({"message": "Project structure created successfully!", "success": True})
    except Exception as e:
        return jsonify({"message": f"Error creating project: {e}", "success": False})

from ..core import create_from_template

@app.route('/create_template', methods=['POST'])
def create_template_web():
    data = request.get_json()
    project_name = data.get('project_name', '')
    template_type = data.get('template_type', '')

    try:
        create_from_template(project_name, template_type, overwrite=True)
        return jsonify({"message": f"Successfully created project '{project_name}' from template '{template_type}'.", "success": True})
    except ValueError as e:
        return jsonify({"message": f"Error: {e}", "success": False})
    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}", "success": False})

@app.route('/preview_docker_compose', methods=['POST'])
def preview_docker_compose():
    data = request.get_json()
    components = data.get('components', [])
    factory = TemplateFactory()
    try:
        template = factory.create_template('docker', components)
        compose_yml = template.get('docker-compose.yml', '# No docker-compose.yml generated')
        return jsonify({"success": True, "compose_yml": compose_yml})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/create_docker', methods=['POST'])
def create_docker_web():
    data = request.get_json()
    project_name = data.get('project_name', '')
    components = data.get('components', [])

    try:
        create_from_template(project_name, 'docker', components, overwrite=True)
        return jsonify({"message": f"Successfully created Docker project '{project_name}' with components {components}.", "success": True})
    except ValueError as e:
        return jsonify({"message": f"Error: {e}", "success": False})
    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}", "success": False})

@app.route('/download_project/<project_name>')
def download_project(project_name):
    project_path = Path(project_name)
    if not project_path.exists() or not project_path.is_dir():
        return jsonify({"message": "Project not found.", "success": False}), 404

    zip_file_name = f"{project_name}.zip"
    zip_file_path = Path(f"/tmp/{zip_file_name}") # Use /tmp for temporary files

    try:
        shutil.make_archive(str(zip_file_path.parent / project_name), 'zip', project_path)
        return send_file(str(zip_file_path), as_attachment=True, download_name=zip_file_name)
    except Exception as e:
        return jsonify({"message": f"Error zipping project: {e}", "success": False}), 500

def run_server():
    port = find_free_port(config_manager.get("web_port_start"))
    print(f"Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)