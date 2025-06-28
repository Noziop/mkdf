from mkdf.templates.docker.base.service_template import DockerService
from typing import Dict, Any, Optional, List

class MongoDBService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'mongo:6.0',
            'container_name': '${PROJECT_NAME:-fullstack}-db',
            'ports': ['27017'],
            'volumes': ['mongo_data:/data/db'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {}