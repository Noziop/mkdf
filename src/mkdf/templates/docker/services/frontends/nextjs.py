from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class NextJSService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        backend_type = next((c for c in components if c in ['fastapi', 'flask', 'django', 'express', 'gofiber', 'laravel', 'symfony']), None)
        
        environment = []
        if backend_type:
            environment.append(f'NEXT_PUBLIC_API_URL=http://{backend_type}:8000/api') # Assuming 8000 for backend for now

        return {
            'build': {
                'context': './frontend',
                'dockerfile': 'Dockerfile'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-frontend',
            'ports': ['3000'],
            'environment': environment,
            'volumes': ['./frontend:/app'],
            'networks': ['app-network']
        }

    def get_dockerfile_content(self):
        return '''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./ 
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
'''

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        if components is None:
            components = []

        backend_type = next((c for c in components if c in ['fastapi', 'flask', 'django', 'express', 'gofiber', 'laravel', 'symfony']), None)
        api_url_display = 'http://localhost/api'
        if backend_type:
            api_url_display = f'http://{backend_type}:8000/api' # Assuming 8000 for backend for now

        return {
            'package.json': '''{
  "name": "nextjs-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18",
    "react-dom": "^18",
    "next": "13.5.4"
  }
}
''',
            'pages/index.js': f'''export default function Home() {{
  return (
    <div>
      <h1>Hello from Next.js!</h1>
      <p>Backend API URL: {{process.env.NEXT_PUBLIC_API_URL || '{api_url_display}'}}</p>
    </div>
  )
}}
'''
        }
