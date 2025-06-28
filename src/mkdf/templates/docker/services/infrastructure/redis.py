from mkdf.templates.docker.base.service_template import DockerService

class RedisService(DockerService):
    def get_service_config(self):
        return {
            'image': 'redis:7-alpine',
            'container_name': '${PROJECT_NAME:-fullstack}-redis',
            'ports': ['6379'],
            'volumes': ['redis_data:/data'],
            'networks': ['app-network']
        }