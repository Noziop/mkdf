from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class MonitoringService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {}

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {
            'prometheus.yml': '''global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
'''
        }