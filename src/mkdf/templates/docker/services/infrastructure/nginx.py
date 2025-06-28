from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class NginxService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            'image': 'nginx:1.25-alpine',
            'container_name': '${PROJECT_NAME:-fullstack}-proxy',
            'ports': ['80:80'],
            'volumes': ['./nginx.conf:/etc/nginx/nginx.conf:ro'],
            'depends_on': ['backend', 'frontend'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        return {
            'nginx.conf': '''events {}

http {
    server {
        listen 80;

        location /api/ {
            proxy_pass http://backend:8000;
        }

        location / {
            proxy_pass http://frontend:3000;
        }
    }
}
'''
        }