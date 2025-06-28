from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class CeleryService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'build': {
                'context': './backend'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-celery',
            'command': ['celery', '-A', 'app.celery', 'worker', '--loglevel=info'],
            'volumes': ['./backend:/app'],
            'depends_on': ['redis'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {}