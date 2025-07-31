from mkdf.templates.docker.base.service_template import DockerService
from typing import Optional, List, Dict, Any

class GrafanaService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        config = {
            'image': 'grafana/grafana:10.1.5',
            'container_name': '${PROJECT_NAME:-fullstack}-grafana',
            'ports': ['3001:3000'],
            'volumes': ['grafana_data:/var/lib/grafana'],
            'environment': [
                'GF_SECURITY_ADMIN_PASSWORD=admin',
                'GF_USERS_ALLOW_SIGN_UP=false'
            ],
            'networks': ['app-network']
        }
        
        # Add datasources volume if Loki or Prometheus are present
        if components and ('loki' in components or 'prometheus' in components):
            config['volumes'].append('./grafana/datasources.yaml:/etc/grafana/provisioning/datasources/datasources.yaml')
        
        # Add depends_on for monitoring services
        depends_on = []
        if components:
            if 'prometheus' in components:
                depends_on.append('prometheus')
            if 'loki' in components:
                depends_on.append('loki')
        
        if depends_on:
            config['depends_on'] = depends_on
            
        return config

    def get_dockerfile_content(self) -> Optional[str]:
        return None

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        files = {}
        
        # Only add datasources if Loki or Prometheus are in components
        if components and ('loki' in components or 'prometheus' in components):
            datasources = []
            
            if 'prometheus' in components:
                datasources.append({
                    'name': 'Prometheus',
                    'type': 'prometheus',
                    'access': 'proxy',
                    'url': 'http://prometheus:9090',
                    'isDefault': True
                })
            
            if 'loki' in components:
                datasources.append({
                    'name': 'Loki',
                    'type': 'loki',
                    'access': 'proxy',
                    'url': 'http://loki:3100',
                    'isDefault': False if 'prometheus' in components else True
                })
            
            if datasources:
                import json
                files['datasources.yaml'] = f'''apiVersion: 1

datasources:
{json.dumps(datasources, indent=2)}
'''
        
        return files