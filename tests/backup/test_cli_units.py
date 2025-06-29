import pytest
from unittest.mock import MagicMock, patch
import typer

from mkdf.cli.commands.create import create_command
from mkdf.cli.models.mappings import create_template_mapping, create_component_mapping
from mkdf.cli.validators.path import get_project_path
from mkdf.cli.interfaces.guided_creation import guided_template_selection, guided_docker_combo, guided_create_mode

@pytest.fixture
def mock_all_cli_dependencies(mocker, tmp_path):
    mocker.patch('src.mkdf.core.create_from_template')
    mocker.patch('src.mkdf.core.create_from_pattern')
    mocker.patch('src.mkdf.cli.ui.panels.print_success_confirmation')
    mocker.patch('src.mkdf.cli.ui.tables.show_templates_table')
    mocker.patch('src.mkdf.cli.ui.tables.show_docker_components_table')
    mocker.patch('src.mkdf.cli.validators.path.get_project_path', return_value=str(tmp_path / "test_projects"))
    mocker.patch('src.mkdf.cli.models.ports.get_interactive_port_config', return_value={})
    mocker.patch('typer.confirm', return_value=True)
    mocker.patch('os.system') # Mock os.system('clear')

def test_create_command_function_guided_mode(mock_all_cli_dependencies, mocker):
    mock_guided_create_mode = mocker.patch('src.mkdf.cli.interfaces.guided_creation.guided_create_mode')
    create_command(
        project_name=None,
        template_or_combo=None,
        components=None,
        force=False,
        verbose=False,
        backend_port=8000,
        frontend_port=3000,
        db_port=None,
        redis_port=6379,
        subnet="172.18.0.0/16",
        prometheus_port=9090,
        grafana_port=3001,
        traefik_port=80,
        traefik_dashboard_port=8080,
    )
    mock_guided_create_mode.assert_called_once_with()

def test_create_command_function_expert_mode_template(mock_all_cli_dependencies, mocker):
    mock_expert_create_mode = mocker.patch('src.mkdf.cli.interfaces.expert_creation.expert_create_mode')
    create_command(
        project_name="myproject",
        template_or_combo="react",
        components=None,
        force=False,
        verbose=False,
        backend_port=8000,
        frontend_port=3000,
        db_port=None,
        redis_port=6379,
        subnet="172.18.0.0/16",
        prometheus_port=9090,
        grafana_port=3001,
        traefik_port=80,
        traefik_dashboard_port=8080,
    )
    mock_expert_create_mode.assert_called_once_with(
        "myproject", "react", None, False, False, 8000, 3000, None, 6379, "172.18.0.0/16", 9090, 3001, 80, 8080, overwrite=False
    )

def test_create_command_function_expert_mode_docker(mock_all_cli_dependencies, mocker):
    mock_expert_create_mode = mocker.patch('src.mkdf.cli.interfaces.expert_creation.expert_create_mode')
    create_command(
        project_name="myproject",
        template_or_combo="docker",
        components=["fastapi", "vue"],
        force=True,
        verbose=True,
        backend_port=8080,
        frontend_port=3001,
        db_port=5433,
        redis_port=6380,
        subnet="172.19.0.0/16",
        prometheus_port=9091,
        grafana_port=3002,
        traefik_port=81,
        traefik_dashboard_port=8081,
    )
    mock_expert_create_mode.assert_called_once_with(
        "myproject", "docker", ["fastapi", "vue"], True, True, 8080, 3001, 5433, 6380, "172.19.0.0/16", 9091, 3002, 81, 8081, overwrite=True
    )

def test_template_mapping_functions():
    template_map = create_template_mapping()
    assert "simple" in template_map.values()
    assert "react" in template_map.values()
    assert "fastapi" in template_map.values()
    assert "laravel" in template_map.values()
    assert "static" in template_map.values()
    assert "1" in template_map # Check if numeric keys are present

def test_component_mapping_functions():
    component_map = create_component_mapping()
    assert "fastapi" in component_map.values()
    assert "vue" in component_map.values()
    assert "postgresql" in component_map.values()
    assert "redis" in component_map.values()
    assert "nginx" in component_map.values()
    assert "1" in component_map # Check if numeric keys are present

def test_path_validation_default_path(mocker):
    mocker.patch('os.path.expanduser', return_value='/home/user')
    mocker.patch('pathlib.Path.mkdir')
    path = get_project_path()
    assert path.startswith('/home/user/projects')

def test_path_validation_custom_absolute_path(mocker):
    mocker.patch('os.path.expanduser', return_value='/custom/path')
    mocker.patch('pathlib.Path.mkdir')
    path = get_project_path(project_name="myproject")
    assert path.endswith('/custom/path/myproject')

def test_guided_template_selection(mock_all_cli_dependencies, mocker):
    mock_typer_prompt = mocker.patch('typer.prompt', return_value="simple")
    mock_create_from_template = mocker.patch('src.mkdf.core.create_from_template')
    
    guided_template_selection("test_project", "/tmp/test_path")
    
    mock_typer_prompt.assert_called_once_with("\nSelect template (name)", type=str)
    mock_create_from_template.assert_called_once_with(
        "test_project", "simple", None, base_path="/tmp/test_path", overwrite=False
    )

def test_guided_docker_combo(mock_all_cli_dependencies, mocker):
    mock_typer_prompt = mocker.patch('typer.prompt')
    mock_typer_prompt.side_effect = ["fastapi vue", "n"] # Components, then no custom ports
    mock_create_from_template = mocker.patch('mkdf.core.create_from_template')
    
    guided_docker_combo("test_docker_project", "/tmp/test_path")
    
    mock_typer_prompt.assert_any_call("\nSelect components (space-separated)", type=str)
    mock_create_from_template.assert_called_once_with(
        "test_docker_project", "docker", ["fastapi", "vue"], base_path="/tmp/test_path", port_config={}, overwrite=False
    )

def test_guided_create_mode_template_flow(mock_all_cli_dependencies, mocker):
    mock_typer_prompt = mocker.patch('typer.prompt')
    mock_typer_prompt.side_effect = [
        "myguidedproject", # Project name
        "template",        # Template or Docker combo
        "simple"           # Template name
    ]
    mock_guided_template_selection = mocker.patch('src.mkdf.cli.interfaces.guided_creation.guided_template_selection')

    guided_create_mode()

    mock_typer_prompt.assert_any_call("Project name")
    mock_typer_prompt.assert_any_call("Template or Docker combo", type=typer.click.Choice(['template', 'docker', 't', 'd']), show_choices=True)
    mock_guided_template_selection.assert_called_once_with(project_name="myguidedproject", project_path=mocker.ANY, overwrite=False)

def test_guided_create_mode_docker_flow(mock_all_cli_dependencies, mocker):
    mock_typer_prompt = mocker.patch('typer.prompt')
    mock_typer_prompt.side_effect = [
        "myguideddockerproject", # Project name
        "docker",                # Template or Docker combo
        "fastapi vue",           # Components
        "n"                      # No custom ports
    ]
    mock_guided_docker_combo = mocker.patch('mkdf.cli.interfaces.guided_creation.guided_docker_combo')

    guided_create_mode()

    mock_typer_prompt.assert_any_call("Project name")
    mock_typer_prompt.assert_any_call("Template or Docker combo", type=typer.click.Choice(['template', 'docker', 't', 'd']), show_choices=True)
    mock_guided_docker_combo.assert_called_once_with(project_name="myguideddockerproject", project_path=mocker.ANY, overwrite=False)
