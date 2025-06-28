from mkdf.templates.docker.base.service_template import DockerService

class TraefikService(DockerService):
    def get_service_config(self):
        return {
            'image': 'traefik:v3.0',
            'container_name': '${PROJECT_NAME:-fullstack}-traefik',
            'command': ['--configFile=/traefik.yml'],
            'ports': ['80:80', '443:443', '8080:8080'],
            'volumes': [
                '/var/run/docker.sock:/var/run/docker.sock:ro',
                './traefik/traefik.yml:/traefik.yml:ro'
            ],
            'networks': ['app-network']
        }

    def get_files(self):
        return {
            'traefik.yml': '''api:
  dashboard: true
  insecure: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
'''
        }