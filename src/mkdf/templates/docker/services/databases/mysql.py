from mkdf.templates.docker.base.service_template import DockerService
from typing import Dict, Any, Optional, List

class MySQLService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'mysql:8.0',
            'container_name': '${PROJECT_NAME:-fullstack}-db',
            'environment': [
                'MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD:-rootpassword}',
                'MYSQL_DATABASE=${MYSQL_DATABASE:-dbname}',
                'MYSQL_USER=${MYSQL_USER:-user}',
                'MYSQL_PASSWORD=${MYSQL_PASSWORD:-password}'
            ],
            'ports': ['3306'],
            'volumes': ['mysql_data:/var/lib/mysql'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {}