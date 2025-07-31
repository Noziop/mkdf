from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class VueService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        backend_type = next((c for c in components if c in ['fastapi', 'flask', 'django', 'express', 'gofiber', 'laravel', 'symfony']), None)
        
        environment = ['VITE_API_URL=http://localhost/api']
        if backend_type:
            environment[0] = f'VITE_API_URL=http://{backend_type}:8000/api' # Assuming 8000 for backend for now

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

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
'''

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        if components is None:
            components = []

        backend_type = next((c for c in components if c in ['fastapi', 'flask', 'django', 'express', 'gofiber', 'laravel', 'symfony']), None)
        api_url = 'http://localhost/api'
        if backend_type:
            api_url = f'http://{backend_type}:8000/api' # Assuming 8000 for backend for now

        return {
            'package.json': '''{
  "name": "vue-app",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.4"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.4.0",
    "vite": "^4.4.5"
  }
}''',
            'vite.config.js': f'''import {{ defineConfig }} from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({{
  plugins: [vue()],
  server: {{
    host: '0.0.0.0',
    port: 3000
  }}
}})
''',
            'index.html': '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vue App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>''',
            'src/main.js': '''import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
''',
            'src/App.vue': f'''<template>
  <div id="app">
    <h1>Hello Vue!</h1>
    <p>Your Vue app is running successfully.</p>
    <p>Backend API URL: {api_url}</p>
  </div>
</template>

<script>
export default {{
  name: 'App'
}}
</script>

<style>
#app {{
  text-align: center;
  padding: 20px;
  font-family: Avenir, Helvetica, Arial, sans-serif;}}
</style>
'''
        }