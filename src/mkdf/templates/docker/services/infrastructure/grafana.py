from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class GrafanaService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'grafana/grafana:10.1.5',
            'container_name': '${PROJECT_NAME:-fullstack}-grafana',
            'ports': ['3001:3000'],
            'volumes': ['grafana_data:/var/lib/grafana'],
            'depends_on': ['prometheus'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {}