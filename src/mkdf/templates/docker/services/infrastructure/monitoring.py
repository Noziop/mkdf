from mkdf.templates.docker.base.service_template import DockerService

class MonitoringService(DockerService):
    def get_service_config(self):
        return {}

    def get_files(self):
        return {
            'prometheus.yml': '''global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
'''
        }