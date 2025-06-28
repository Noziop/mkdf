from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class RedisService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'redis:7-alpine',
            'container_name': '${PROJECT_NAME:-fullstack}-redis',
            'ports': ['6379'],
            'volumes': ['redis_data:/data'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {}