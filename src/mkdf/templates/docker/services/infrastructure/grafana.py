from mkdf.templates.docker.base.service_template import DockerService

class GrafanaService(DockerService):
    def get_service_config(self):
        return {
            'image': 'grafana/grafana:10.1.5',
            'container_name': '${PROJECT_NAME:-fullstack}-grafana',
            'ports': ['3001:3000'],
            'volumes': ['grafana_data:/var/lib/grafana'],
            'depends_on': ['prometheus'],
            'networks': ['app-network']
        }