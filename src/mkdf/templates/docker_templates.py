import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, TypedDict

class PortConfig(TypedDict, total=False):
    backend: int
    frontend: int
    database: int
    redis: int
    subnet: str
    prometheus: int
    grafana: int
    traefik: int
    traefik_dashboard: int

ProjectStructure = Dict[str, Union[str, Dict[str, Any]]]

DOCKER_COMPONENT_CATEGORIES = {
    "Backend": ["fastapi", "flask", "express", "gofiber", "laravel", "django", "symfony"],
    "Frontend": ["vue", "react", "svelte", "angular", "nextjs", "nuxtjs"],
    "Fullstack": ["laravel", "django", "symfony"],
    "Database": ["postgresql", "mysql", "mongodb"],
    "Cache/Queue": ["redis", "celery", "rabbitmq"],
    "Proxy": ["nginx", "traefik"],
    "Monitoring": ["prometheus", "grafana"]
}



from mkdf.templates.docker.registry import get_service

def get_docker_template(
    components: Optional[List[str]] = None,
    project_name: Optional[str] = None,
    port_config: Optional[PortConfig] = None
) -> ProjectStructure:
    """Generate Docker template with configurable ports and subnet."""
    
    if components is None:
        components = []
    if project_name is None:
        project_name = "fullstack-app"
    if port_config is None:
        port_config = {
            'backend': 8000,
            'frontend': 3000,
            'database': 5432,
            'redis': 6379,
            'subnet': '172.18.0.0/16',
            'prometheus': 9090,
            'grafana': 3001,
            'traefik': 80,
            'traefik_dashboard': 8080,
        }

    project_structure = {}
    docker_compose_services = {}
    docker_compose_volumes = {}
    network_name = f"{project_name}_app-network"
    
    docker_compose_networks = {
        network_name: {
            'driver': 'bridge',
            'ipam': {
                'config': [{
                    'subnet': port_config.get('subnet', '172.18.0.0/16')
                }]
            }
        }
    }

    # Root level files
    project_structure['.env'] = f'''PROJECT_NAME={project_name}
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=dbname
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=dbname
MYSQL_USER=user
MYSQL_PASSWORD=password
SECRET_KEY=your-super-secret-key-here
DEBUG=true
'''

    for component in components:
        service = get_service(component)
        service_config = service.get_service_config(components)

        # Apply port configuration
        if 'ports' in service_config:
            port_key = None
            if component in ['fastapi', 'flask', 'django', 'laravel', 'symfony', 'express', 'gofiber']:
                port_key = 'backend'
            elif component in ['vue', 'angular', 'react', 'svelte', 'nextjs', 'nuxtjs']:
                port_key = 'frontend'
            elif component in ['postgresql', 'mysql']:
                port_key = 'database'
            elif component == 'redis':
                port_key = 'redis'
            elif component == 'traefik':
                traefik_port = port_config.get('traefik', 80)
                traefik_dashboard = port_config.get('traefik_dashboard', 8080)
                service_config['ports'] = [
                    f"{traefik_port}:80",
                    "443:443",
                    f"{traefik_dashboard}:8080"
                ]
            elif component == 'prometheus':
                prometheus_port = port_config.get('prometheus', 9090)
                service_config['ports'] = [f"{prometheus_port}:9090"]
            elif component == 'grafana':
                grafana_port = port_config.get('grafana', 3001)
                service_config['ports'] = [f"{grafana_port}:3000"]
            
            if port_key:
                # Extract the internal port from the service_config, assuming it's always the last part after a colon, or the whole string if no colon.
                internal_port = service_config['ports'][0].split(':')[-1]
                # Get the external port from port_config, defaulting to the internal port if not specified.
                external_port = port_config.get(port_key, internal_port)
                
                service_config['ports'] = [f"{external_port}:{internal_port}"]
            else:
                # If no port_key, and the service_config only has an internal port, map it to internal:internal
                if ':' not in service_config['ports'][0]:
                    service_config['ports'] = [f"{service_config['ports'][0]}:{service_config['ports'][0]}"]

        if 'networks' in service_config:
            service_config['networks'] = [network_name]

        docker_compose_services[component] = service_config

        if 'volumes' in service_config:
            for volume_mapping in service_config['volumes']:
                if ':' in volume_mapping:
                    volume_name = volume_mapping.split(':')[0]
                    if not volume_name.startswith('.') and not volume_name.startswith('/'):
                        docker_compose_volumes[volume_name] = None

        # Determine the base path for files and Dockerfile
        # For services with 'build' context, use that as the base path
        # Otherwise, use the component name as the base path
        component_base_path = service_config.get('build', {}).get('context', component).lstrip('./')

        files = service.get_files(components)
        for file_path, content in files.items():
            full_path = Path(component_base_path) / file_path
            current_dict = project_structure
            for i, part in enumerate(full_path.parts):
                if i == len(full_path.parts) - 1:
                    current_dict[part] = content
                else:
                    if part not in current_dict or not isinstance(current_dict[part], dict):
                        current_dict[part] = {}
                    current_dict = current_dict[part]

        dockerfile_content = service.get_dockerfile_content()
        if dockerfile_content:
            dockerfile_path = Path(component_base_path) / 'Dockerfile'
            current_dict = project_structure
            for i, part in enumerate(dockerfile_path.parts):
                if i == len(dockerfile_path.parts) - 1:
                    current_dict[part] = dockerfile_content
                else:
                    if part not in current_dict or not isinstance(current_dict[part], dict):
                        current_dict[part] = {}
                    current_dict = current_dict[part]

    # Create data directories
    data_dirs = {}
    for component in components:
        if component == 'postgresql':
            data_dirs['data/postgresql'] = {}
            data_dirs['data/postgresql/.gitkeep'] = ''
        elif component == 'redis':
            data_dirs['data/redis'] = {}
            data_dirs['data/redis/.gitkeep'] = ''
        elif component == 'mysql':
            data_dirs['data/mysql'] = {}
            data_dirs['data/mysql/.gitkeep'] = ''
        elif component == 'mongodb':
            data_dirs['data/mongodb'] = {}
            data_dirs['data/mongodb/.gitkeep'] = ''
        elif component == 'prometheus':
            data_dirs['data/prometheus'] = {}
            data_dirs['data/prometheus/.gitkeep'] = ''
        elif component == 'grafana':
            data_dirs['data/grafana'] = {}
            data_dirs['data/grafana/.gitkeep'] = ''

    # Add data directories to project structure
    for data_path, content in data_dirs.items():
        parts = Path(data_path).parts
        current_dict = project_structure
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current_dict[part] = content
            else:
                if part not in current_dict:
                    current_dict[part] = {}
                current_dict = current_dict[part]

    # Construct docker-compose.yml
    compose_content = ["version: '3.8'", "", "services:"]
    for service_name, service_config in docker_compose_services.items():
        compose_content.append(f"  {service_name}:")
        for key, value in service_config.items():
            if key == 'build' and isinstance(value, dict):
                compose_content.append("    build:")
                compose_content.append(f"      context: {value['context']}")
                compose_content.append(f"      dockerfile: {value['dockerfile']}")
            elif isinstance(value, list):
                compose_content.append(f"    {key}:")
                for item in value:
                    compose_content.append(f"      - {item}")
            elif isinstance(value, dict):
                compose_content.append(f"    {key}:")
                for sub_key, sub_value in value.items():
                    compose_content.append(f"      {sub_key}: {sub_value}")
            else:
                compose_content.append(f"    {key}: {value}")
        compose_content.append("")

    if docker_compose_volumes:
        compose_content.append("volumes:")
        for volume_name in docker_compose_volumes.keys():
            compose_content.append(f"  {volume_name}:")
        compose_content.append("")

    compose_content.append("networks:")
    for network_name_key, network_config in docker_compose_networks.items():
        compose_content.append(f"  {network_name_key}:")
        for key, value in network_config.items():
            if isinstance(value, dict):
                compose_content.append(f"    {key}:")
                for sub_key, sub_value in value.items():
                    compose_content.append(f"      {sub_key}: {sub_value}")
            else:
                compose_content.append(f"    {key}: {value}")

    project_structure['docker-compose.yml'] = "\n".join(compose_content)

    return project_structure