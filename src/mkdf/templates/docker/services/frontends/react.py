from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class ReactService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        backend_type = next((c for c in components if c in ['fastapi', 'flask', 'django', 'express', 'gofiber', 'laravel', 'symfony']), None)
        
        environment = []
        if backend_type:
            environment.append(f'REACT_APP_API_URL=http://{backend_type}:8000/api') # Assuming 8000 for backend for now

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

CMD ["npm", "start"]
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
  "name": "react-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}''',
            'src/App.js': f'''import React from 'react';

function App() {{
  return (
    <div>
      <h1>Hello from React!</h1>
      <p>Backend API URL: {{process.env.REACT_APP_API_URL || '{api_url_display}'}}</p>
    </div>
  );
}}

export default App;
''',
            'src/index.js': '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''',
            'public/index.html': '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>React App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
'''
        }
