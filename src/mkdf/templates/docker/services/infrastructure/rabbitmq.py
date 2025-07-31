from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class RabbitMQService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'rabbitmq:3.12-management-alpine',
            'container_name': '${PROJECT_NAME:-fullstack}-rabbitmq',
            'hostname': 'rabbitmq',
            'ports': ['5672:5672', '15672:15672'],
            'environment': [
                'RABBITMQ_DEFAULT_USER=${RABBITMQ_USER:-admin}',
                'RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASSWORD:-password}',
                'RABBITMQ_DEFAULT_VHOST=${RABBITMQ_VHOST:-/}'
            ],
            'volumes': ['rabbitmq_data:/var/lib/rabbitmq'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {}
