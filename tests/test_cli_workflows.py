import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
import os
from pathlib import Path
import shutil
import typer

from mkdf.cli.parsers.main_parser import app
from mkdf.core import create_from_template, create_from_pattern
from mkdf.cli.interfaces.guided_creation import guided_create_mode
from mkdf.cli.interfaces.interactive_actions import interactive_create_from_template, interactive_create_docker_combo, interactive_create_from_pattern
from mkdf.cli.commands.create import create_command
from mkdf.cli.commands.pattern import pattern_command
from mkdf.cli.commands.interactive import interactive_command

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_all_dependencies(mocker, tmp_path):
    # Mock file system operations to prevent actual file creation
    mocker.patch('src.mkdf.fs.dir_creator.create_directory', return_value=None)
    mocker.patch('src.mkdf.fs.file_creator.create_file', return_value=None)
    mocker.patch('src.mkdf.cli.interfaces.expert_creation.Path.exists', return_value=False)
    mocker.patch('src.mkdf.cli.interfaces.guided_creation.Path.exists', return_value=False)
    mocker.patch('src.mkdf.cli.interfaces.interactive_actions.Path.mkdir', return_value=None)
    mocker.patch('src.mkdf.cli.interfaces.interactive_actions.Path.exists', return_value=False)
    mocker.patch('src.mkdf.cli.interfaces.interactive_actions.os.system', return_value=0) # Mock os.system('clear')

    # Mock typer.confirm to always return True for overwriting
    mocker.patch('typer.confirm', return_value=True)

    # Mock get_project_path to always return a temporary path
    mocker.patch('src.mkdf.cli.validators.path.get_project_path', return_value=str(tmp_path / "test_projects"))

    # Mock print_success_confirmation to avoid Rich output during tests
    mocker.patch('src.mkdf.cli.ui.panels.print_success_confirmation', return_value=None)

    # Mock show_rainbow_banner to avoid Rich output during tests
    mocker.patch('src.mkdf.cli.ui.banner.show_rainbow_banner', return_value=None)

    # Mock time.sleep
    mocker.patch('time.sleep', return_value=None)

    # Mock create_template_mapping and create_component_mapping for interactive modes
    mocker.patch('src.mkdf.cli.models.mappings.create_template_mapping', return_value={'1': 'simple', 'simple': 'simple'})
    mocker.patch('src.mkdf.cli.models.mappings.create_component_mapping', return_value={'1': 'fastapi', 'fastapi': 'fastapi', '2': 'vue', 'vue': 'vue', '3': 'postgresql', 'postgresql': 'postgresql'})

    mocker.patch('src.mkdf.utils.find_free_subnet', return_value='172.25.0.0/16')
    mocker.patch('src.mkdf.utils.find_free_port', side_effect=lambda x: x + 1000) # Mock find_free_port to return a predictable value

    # Mock get_interactive_port_config to return a default dictionary
    mocker.patch('src.mkdf.cli.models.ports.get_interactive_port_config', return_value={})

    # Patch the functions that perform the actual creation logic within the CLI commands
    mock_expert_create_mode = mocker.patch('src.mkdf.cli.interfaces.expert_creation.expert_create_mode')
    mock_guided_create_mode = mocker.patch('src.mkdf.cli.interfaces.guided_creation.guided_create_mode')
    mock_interactive_create_from_template = mocker.patch('src.mkdf.cli.interfaces.interactive_actions.interactive_create_from_template')
    mock_interactive_create_docker_combo = mocker.patch('src.mkdf.cli.interfaces.interactive_actions.interactive_create_docker_combo')
    mock_interactive_create_from_pattern = mocker.patch('src.mkdf.cli.interfaces.interactive_actions.interactive_create_from_pattern')
    mock_pattern_command_create_from_pattern = mocker.patch('mkdf.core.create_from_pattern') # For direct pattern command

    return (
        mock_expert_create_mode,
        mock_guided_create_mode,
        mock_interactive_create_from_template,
        mock_interactive_create_docker_combo,
        mock_interactive_create_from_pattern,
        mock_pattern_command_create_from_pattern,
    )


def test_template_creation_workflow(mock_all_dependencies, mocker):
    mock_expert_create_mode, _, _, _, _, _ = mock_all_dependencies
    # Test "mkdf create myproject react" end-to-end
    result = runner.invoke(app, ["create", "myproject", "react"])
    assert result.exit_code == 0
    mock_expert_create_mode.assert_called_once_with(
        "myproject", "react", None, force=False, verbose=False, backend_port=8000 + 1000, frontend_port=3000 + 1000, db_port=None, redis_port=6379 + 1000, subnet="172.25.0.0/16", prometheus_port=9090 + 1000, grafana_port=3001 + 1000, traefik_port=80 + 1000, traefik_dashboard_port=8080 + 1000, traefik_hhtps_port=443 + 1000, project_path=".", overwrite=False
    )

def test_docker_combo_workflow(mock_all_dependencies, mocker):
    mock_expert_create_mode, _, _, _, _, _ = mock_all_dependencies
    # Test "mkdf create myproject docker fastapi vue postgresql"
    result = runner.invoke(app, ["create", "myproject", "docker", "fastapi", "vue", "postgresql"])
    assert result.exit_code == 0
    mock_expert_create_mode.assert_called_once_with(
        "myproject", "docker", ["fastapi", "vue", "postgresql"], force=False, verbose=False, backend_port=8000 + 1000, frontend_port=3000 + 1000, db_port=None, redis_port=6379 + 1000, subnet="172.25.0.0/16", prometheus_port=9090 + 1000, grafana_port=3001 + 1000, traefik_port=80 + 1000, traefik_dashboard_port=8080 + 1000, traefik_hhtps_port=443 + 1000, project_path=".", overwrite=False
    )

def test_guided_mode_workflow(mock_all_dependencies, mocker):
    _, mock_guided_create_mode, _, _, _, _ = mock_all_dependencies
    # Test guided creation with mocked user inputs
    # Inputs: project_name, project_path (empty for default), template_or_combo, template_name
    result = runner.invoke(app, ["create"], input="myguidedproject\n\ntemplate\nsimple\n")
    assert result.exit_code == 0
    mock_guided_create_mode.assert_called_once_with(project_name="myguidedproject")

def test_interactive_mode_workflow(mock_all_dependencies, mocker):
    _, _, mock_interactive_create_from_template, _, _, _ = mock_all_dependencies
    # Test interactive template selection
    # Inputs: main_menu_choice (2 for template), template_choice (1 for simple), project_name, project_path (empty for default), confirm_creation, exit_interactive_mode
    result = runner.invoke(app, ["interactive"], input="2\n1\nmyinteractiveproject\n\ny\n0\n")
    assert result.exit_code == 0
    mock_interactive_create_from_template.assert_called_once_with(
        banner_callback=mocker.ANY
    )

def test_interactive_docker_combo_workflow(mock_all_dependencies, mocker):
    _, _, _, mock_interactive_create_docker_combo, _, _ = mock_all_dependencies
    # Test interactive Docker combo creation
    # Inputs: main_menu_choice (3 for docker combo), components (1 2 3 for fastapi vue postgresql), project_name, project_path (empty for default), custom_ports (n), confirm_creation, exit_interactive_mode
    result = runner.invoke(app, ["interactive"], input="3\n1 2 3\nmydockercombo\n\nn\ny\n0\n")
    assert result.exit_code == 0
    mock_interactive_create_docker_combo.assert_called_once_with(
        banner_callback=mocker.ANY
    )

def test_pattern_creation_workflow(mock_all_dependencies, mocker):
    _, _, _, _, _, mock_pattern_command_create_from_pattern = mock_all_dependencies
    # Test "mkdf pattern myproject/{src/,docs/,README.md}"
    result = runner.invoke(app, ["pattern", "myproject/{src/,docs/,README.md}"])
    assert result.exit_code == 0
    mock_pattern_command_create_from_pattern.assert_called_once_with(
        "myproject/{src/,docs/,README.md}", overwrite=False
    )

def test_interactive_pattern_creation_workflow(mock_all_dependencies, mocker):
    _, _, _, _, mock_interactive_create_from_pattern, _ = mock_all_dependencies
    # Test interactive pattern creation
    # Inputs: main_menu_choice (1 for pattern), pattern, project_path (empty for default), confirm_creation, exit_interactive_mode
    result = runner.invoke(app, ["interactive"], input="1\nmyinteractivepattern/{src/,docs/}\n\ny\n0\n")
    assert result.exit_code == 0
    mock_interactive_create_from_pattern.assert_called_once()