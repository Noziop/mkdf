from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class TraefikService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'traefik:v3.0',
            'container_name': '${PROJECT_NAME:-fullstack}-traefik',
            'command': [
                '--configFile=/traefik.yml',
                '--providers.docker.exposedByDefault=false',
                '--entrypoints.web.address=:80',
                '--entrypoints.websecure.address=:443',
                '--api.dashboard=true',
                '--api.insecure=true'
            ],
            'volumes': [
                '/var/run/docker.sock:/var/run/docker.sock:ro',
                './traefik/traefik.yml:/traefik.yml:ro'
            ],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {
            'traefik.yml': '''api:
  dashboard: true
  insecure: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
'''
        }