from typing import List, Dict, Any, Optional
from pathlib import Path
from ..docker.registry import get_service
from ..docker.base.db_utils import detect_database_service
from ...utils import find_free_port, find_free_subnet
from ...config.config_manager import ConfigManager
import ipaddress
import socket

config_manager = ConfigManager()

class PortConfig(dict):
    pass

class DockerfileFactory:
    @staticmethod
    def create(component: str, components: Optional[List[str]] = None) -> Optional[str]:
        service = get_service(component)
        return service.get_dockerfile_content()

ProjectStructure = Dict[str, Any]

class DockerComposeFactory:
    @staticmethod
    def create(
        components: Optional[List[str]] = None,
        project_name: Optional[str] = None,
        port_config: Optional[PortConfig] = None
    ) -> ProjectStructure:
        """Generate Docker template with configurable ports and subnet."""
        print(f"DEBUG: components at start of create: {components}")
        if components is None:
            components = []
        if project_name is None:
            project_name = "fullstack-app"
        if port_config is None:
            port_config = {}

        # Default port mappings
        default_ports = {
            'fastapi': 8000, 'flask': 5000, 'django': 8000, 'express': 3000,
            'vue': 3000, 'react': 3000, 'angular': 4200, 'svelte': 5173,
            'postgresql': 5432, 'mysql': 3306, 'mariadb': 3306, 'mongodb': 27017,
            'redis': 6379, 'prometheus': 9090, 'grafana': 3001, 'traefik': 80, 'traefik_dashboard': 8080
        }

        # Identify backend, frontend, and database for port configuration
        backend_type = next((c for c in components if c in ['fastapi', 'flask', 'django', 'express']), None)
        frontend_type = next((c for c in components if c in ['vue', 'react', 'angular', 'svelte']), None)
        db_config = detect_database_service(components)
        if db_config:
            print(f"🔍 DEBUG: db_config['env_vars'] = {db_config.get('env_vars')}")
            print(f"🔍 DEBUG: type(db_config['env_vars']) = {type(db_config.get('env_vars'))}")
        database_type = db_config['service_name'] if db_config else {} #None

        # Build port_config with defaults
        final_port_config = {
            'backend': port_config.get('backend', find_free_port(default_ports.get(backend_type, 8000))),
            'frontend': port_config.get('frontend', find_free_port(default_ports.get(frontend_type, 3000))),
            'database': port_config.get('database', find_free_port(default_ports.get(database_type, 5432) if database_type else 5432)),
            'redis': port_config.get('redis', find_free_port(default_ports.get('redis', 6379))),
            'traefik': port_config.get('traefik', find_free_port(default_ports.get('traefik', 80))),
            'traefik_dashboard': port_config.get('traefik_dashboard', find_free_port(default_ports.get('traefik_dashboard', 8080))),
            'subnet': port_config.get('subnet', find_free_subnet()),
            'prometheus': port_config.get('prometheus', find_free_port(default_ports.get('prometheus', 9090))),
            'grafana': port_config.get('grafana', find_free_port(default_ports.get('grafana', 3001))),
            'traefik_https_port': port_config.get('traefik_https_port', find_free_port(443))
        }
        print(f"DEBUG: Subnet after find_free_subnet: {final_port_config.get('subnet')}")

        project_structure = {}
        docker_compose_services = {}
        docker_compose_volumes = {}
        network_name = f"{project_name}_app-network"
        
        docker_compose_networks = {
            network_name: {
                'driver': 'bridge',
                'ipam': {
                    'config': [{
                        'subnet': final_port_config.get('subnet')
                    }]
                }
            }
        }

        # .env file generation
        env_vars = [f'PROJECT_NAME={project_name}']
        if db_config and 'env_vars' in db_config:
            print(f"🔍 DEBUG: About to extend with: {db_config['env_vars']}")
            env_vars.extend(db_config['env_vars'])
        
        if backend_type:
            env_vars.extend(['SECRET_KEY=your-super-secret-key-here', 'DEBUG=true'])

        project_structure['.env'] = "\n".join(env_vars)


        for component in components:
            service = get_service(component)
            if service is None:
                raise ValueError(f"Service not found for component: {component}")
            print(f"🔍 DEBUG boucle comp in comp: service for {component} type: {type(service)}")
            print(f"DEBUG: service for {component}: {service}")
            service_config = service.get_service_config(components)
            print(f"🔍 service_config type: {type(service_config)}, value: {service_config}")
            print(f"DEBUG: service_config for {component}: {service_config}")

            # Apply port configuration
            port_key = None
            internal_port = None

            if component in ['fastapi', 'flask', 'django', 'express']:
                port_key = 'backend'
                internal_port = default_ports.get(component, 8000)
            elif component in ['vue', 'react', 'angular', 'svelte']:
                port_key = 'frontend'
                internal_port = default_ports.get(component, 3000)
            elif component in ['postgresql', 'mysql', 'mariadb', 'mongodb']:
                port_key = 'database'
                internal_port = default_ports.get(component, 5432)
            elif component == 'redis':
                port_key = 'redis'
                internal_port = default_ports.get(component, 6379)
            
            if port_key:
                external_port = final_port_config.get(port_key)
                print(f"DEBUG: port_key: {port_key}, external_port: {external_port}, internal_port: {internal_port}, type: {type(external_port), type(internal_port), type(port_key)}")
                if external_port is not None:
                    service_config['ports'] = [f"{external_port}:{internal_port}"]
                else:
                    # Fallback to internal port if external is not found (shouldn't happen with find_free_port)
                    service_config['ports'] = [f"{internal_port}:{internal_port}"]

            elif component == 'traefik':
                traefik_port = final_port_config.get('traefik')
                traefik_dashboard_port = final_port_config.get('traefik_dashboard')
                service_config['ports'] = [
                    f"{traefik_port}:80",
                    f"{final_port_config.get('traefik_https_port')}:443", # Assuming 443 is always internal for Traefik
                    f"{traefik_dashboard_port}:8080" # Traefik dashboard
                ]

            # Inject Traefik labels conditionally
            if 'traefik' in components:
                print(f"DEBUG: Adding Traefik labels for component: {component}")
                print(f"DEBUG: port_key: {port_key}, internal_port: {internal_port}")
                labels_to_add = []
                if port_key == 'backend' and internal_port:
                    labels_to_add.extend([
                        "traefik.enable=true",
                        f"traefik.http.routers.{project_name}-backend.rule=Host(`{project_name}.localhost`) && PathPrefix(`/api`)",
                        f"traefik.http.routers.{project_name}-backend.entrypoints=web",
                        f"traefik.http.services.{project_name}-backend.loadbalancer.server.port={internal_port}"
                    ])
                elif port_key == 'frontend' and internal_port:
                    labels_to_add.extend([
                        "traefik.enable=true",
                        f"traefik.http.routers.{project_name}-frontend.rule=Host(`{project_name}.localhost`)",
                        f"traefik.http.routers.{project_name}-frontend.entrypoints=web",
                        f"traefik.http.services.{project_name}-frontend.loadbalancer.server.port={internal_port}"
                    ])
                
                if labels_to_add:
                    if 'labels' not in service_config:
                        service_config['labels'] = []
                    service_config['labels'].extend(labels_to_add)

            if 'networks' in service_config:
                service_config['networks'] = [network_name]

            docker_compose_services[component] = service_config

            if 'volumes' in service_config:
                for volume_mapping in service_config['volumes']:
                    if ':' in volume_mapping:
                        volume_name = volume_mapping.split(':')[0]
                        if not volume_name.startswith('.') and not volume_name.startswith('/'):
                            docker_compose_volumes[volume_name] = None

            component_path = service_config.get('build', {}).get('context', f'./{component}').lstrip('./')
            files = service.get_files(components)
            print(f"🔍 files type: {type(files)}, value: {files}")
            print(f"DEBUG: files for {component}: {files}")
            for file_path, content in files.items():
                full_path = Path(component_path) / file_path
                current_dict = project_structure
                for i, part in enumerate(full_path.parts):
                    if i == len(full_path.parts) - 1:
                        current_dict[part] = content
                    else:
                        if part not in current_dict or not isinstance(current_dict[part], dict):
                            current_dict[part] = {}
                        current_dict = current_dict[part]

            dockerfile_content = DockerfileFactory.create(component, components)
            if dockerfile_content:
                dockerfile_path = Path(component_path) / 'Dockerfile'
                current_dict = project_structure
                for i, part in enumerate(dockerfile_path.parts):
                    if i == len(dockerfile_path.parts) - 1:
                        current_dict[part] = dockerfile_content
                    else:
                        if part not in current_dict or not isinstance(current_dict[part], dict):
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