from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class PromtailService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'grafana/promtail:2.9.2',
            'container_name': '${PROJECT_NAME:-fullstack}-promtail',
            'volumes': [
                './promtail/promtail-config.yaml:/etc/promtail/config.yml',
                '/var/log:/var/log:ro',
                '/var/lib/docker/containers:/var/lib/docker/containers:ro',
                '/var/run/docker.sock:/var/run/docker.sock'
            ],
            'command': ['-config.file=/etc/promtail/config.yml'],
            'depends_on': ['loki'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {
            'promtail-config.yaml': '''server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Docker container logs
  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__: /var/lib/docker/containers/*/*log

    pipeline_stages:
      - json:
          expressions:
            output: log
            stream: stream
            attrs:
      - json:
          expressions:
            tag:
          source: attrs
      - regex:
          expression: (?P<container_name>(?:[^|]*))'
          source: tag
      - timestamp:
          format: RFC3339Nano
          source: time
      - labels:
          stream:
          container_name:
      - output:
          source: output

  # System logs
  - job_name: syslog
    static_configs:
      - targets:
          - localhost
        labels:
          job: syslog
          __path__: /var/log/syslog

  # Application logs (customize as needed)
  - job_name: app_logs
    static_configs:
      - targets:
          - localhost
        labels:
          job: app_logs
          __path__: /var/log/app/*.log
'''
        }
