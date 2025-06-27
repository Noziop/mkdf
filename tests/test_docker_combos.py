import pytest
import os
from mkdf.templates.docker_templates import get_docker_template
from mkdf.fs.dir_creator import create_directory
from mkdf.fs.file_creator import create_file

def _create_from_template_recursive(base_path, template_dict):
    """
    Recursively creates directories and files from a template dictionary.
    """
    for name, content in template_dict.items():
        current_path = os.path.join(base_path, name)
        if isinstance(content, dict):
            create_directory(current_path)
            _create_from_template_recursive(current_path, content)
        elif content is None:
            create_directory(current_path)
        else:
            create_file(current_path, str(content))

def test_fastapi_vue_combo(tmp_path):
    project_name = "test_fastapi_vue"
    components = ["fastapi", "vue"]
    
    template = get_docker_template(components)
    
    project_path = tmp_path / project_name
    create_directory(str(project_path))
    _create_from_template_recursive(str(project_path), template)

    assert (project_path / "backend" / "Dockerfile").exists()
    assert (project_path / "frontend" / "Dockerfile").exists()
    assert (project_path / "docker-compose.yml").exists()
    assert (project_path / "backend" / "app" / "main.py").exists()
    assert (project_path / "backend" / "requirements.txt").exists()
    assert (project_path / "frontend" / "package.json").exists()
    assert (project_path / "frontend" / "vite.config.js").exists()

    with open(project_path / "docker-compose.yml", 'r') as f:
        content = f.read()
        assert "fastapi:" in content
        assert "vue:" in content
        assert "8000" in content # Dynamic port
        assert "3000" in content # Dynamic port

def test_laravel_mysql_traefik_combo(tmp_path):
    project_name = "test_laravel_mysql_traefik"
    components = ["laravel", "mysql", "traefik"]

    template = get_docker_template(components)

    project_path = tmp_path / project_name
    create_directory(str(project_path))
    _create_from_template_recursive(str(project_path), template)

    assert (project_path / "backend" / "Dockerfile").exists()
    assert (project_path / "docker-compose.yml").exists()
    assert (project_path / "backend" / "public" / "index.php").exists()
    assert (project_path / "traefik" / "traefik.yml").exists()

    with open(project_path / "docker-compose.yml", 'r') as f:
        content = f.read()
        assert "laravel:" in content
        assert "mysql:" in content
        assert "traefik:" in content
        assert "80" in content
        assert "3306" in content

def test_django_postgres_redis_monitoring_combo(tmp_path):
    project_name = "test_django_postgres_redis_monitoring"
    components = ["django", "postgresql", "redis", "monitoring"]

    template = get_docker_template(components)

    project_path = tmp_path / project_name
    create_directory(str(project_path))
    _create_from_template_recursive(str(project_path), template)

    assert (project_path / "backend" / "Dockerfile").exists()
    assert (project_path / "docker-compose.yml").exists()
    assert (project_path / "backend" / "manage.py").exists()
    assert (project_path / "monitoring" / "prometheus.yml").exists()
    assert (project_path / "monitoring" / "grafana" / "provisioning" / "dashboards" / "dashboard.yml").exists()

    with open(project_path / "docker-compose.yml", 'r') as f:
        content = f.read()
        assert "django:" in content
        assert "postgresql:" in content
        assert "redis:" in content
        assert "prometheus:" in content
        assert "grafana:" in content
        assert "8000" in content
        assert "5432" in content
        assert "6379" in content
        assert "9090" in content
        assert "3001" in content

def test_gofiber_svelte_nginx_combo(tmp_path):
    project_name = "test_gofiber_svelte_nginx"
    components = ["gofiber", "svelte", "nginx"]

    template = get_docker_template(components)

    project_path = tmp_path / project_name
    create_directory(str(project_path))
    _create_from_template_recursive(str(project_path), template)

    assert (project_path / "backend" / "Dockerfile").exists()
    assert (project_path / "frontend" / "Dockerfile").exists()
    assert (project_path / "nginx" / "Dockerfile").exists()
    assert (project_path / "docker-compose.yml").exists()
    assert (project_path / "backend" / "main.go").exists()
    assert (project_path / "frontend" / "src" / "routes" / "+page.svelte").exists()
    assert (project_path / "nginx" / "conf" / "nginx.conf").exists()

    with open(project_path / "docker-compose.yml", 'r') as f:
        content = f.read()
        assert "gofiber:" in content
        assert "svelte:" in content
        assert "nginx:" in content
        assert "3000" in content
        assert "80" in content