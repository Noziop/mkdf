from mkdf.templates.docker.base.service_template import DockerService
from typing import Dict, Any, Optional, List

class MariaDBService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'mariadb:11',
            'container_name': '${PROJECT_NAME:-fullstack}-db',
            'environment': [
                'MARIADB_ROOT_PASSWORD=${MARIADB_ROOT_PASSWORD:-rootpassword}',
                'MARIADB_DATABASE=${MARIADB_DATABASE:-dbname}',
                'MARIADB_USER=${MARIADB_USER:-user}',
                'MARIADB_PASSWORD=${MARIADB_PASSWORD:-password}'
            ],
            'ports': ['3306'],
            'volumes': ['mariadb_data:/var/lib/mysql'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {}