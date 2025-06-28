from mkdf.templates.docker.base.service_template import DockerService

class PrometheusService(DockerService):
    def get_service_config(self):
        return {
            'image': 'prom/prometheus:v2.47.0',
            'container_name': '${PROJECT_NAME:-fullstack}-prometheus',
            'ports': ['9090:9090'],
            'volumes': ['./prometheus.yml:/etc/prometheus/prometheus.yml'],
            'networks': ['app-network']
        }