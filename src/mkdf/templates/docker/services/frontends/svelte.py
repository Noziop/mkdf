from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class SvelteService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        backend_type = next((c for c in components if c in ['fastapi', 'flask', 'django', 'express', 'gofiber', 'laravel', 'symfony']), None)
        
        environment = []
        if backend_type:
            environment.append(f'VITE_API_URL=http://{backend_type}:8000/api') # Assuming 8000 for backend for now

        return {
            'build': {
                'context': './frontend',
                'dockerfile': 'Dockerfile'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-frontend',
            'ports': ['5173'],
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

EXPOSE 5173

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
  "name": "svelte-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@sveltejs/vite-plugin-svelte": "^2.4.2",
    "svelte": "^4.0.5",
    "vite": "^4.4.5"
  }
}''',
            'vite.config.js': '''import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
})
''',
            'src/App.svelte': f'''<script>
  export let name = 'Svelte';
  const API_URL = import.meta.env.VITE_API_URL || '{api_url_display}';
</script>

<main>
  <h1>Hello {{name}}!</h1>
  <p>Backend API URL: {{API_URL}}</p>
</main>

<style>
  main {{
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }}

  h1 {{
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }}
</style>
'''
        }
