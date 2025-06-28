from mkdf.templates.docker.base.service_template import DockerService
from typing import Dict, Any, Optional, List

class PostgreSQLService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'postgres:15-alpine',
            'container_name': '${PROJECT_NAME:-fullstack}-db',
            'environment': [
                'POSTGRES_USER=${POSTGRES_USER:-user}',
                'POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-password}',
                'POSTGRES_DB=${POSTGRES_DB:-dbname}'
            ],
            'ports': ['5432'],
            'volumes': ['postgres_data:/var/lib/postgresql/data'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {}