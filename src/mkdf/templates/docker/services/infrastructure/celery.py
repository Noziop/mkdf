from mkdf.templates.docker.base.service_template import DockerService

class CeleryService(DockerService):
    def get_service_config(self):
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