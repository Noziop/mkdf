from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service
import json

class ExpressService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        db_config = detect_database_service(components)
        environment = ['NODE_ENV=development']
        depends_on = []

        if db_config:
            environment.append(f'DATABASE_URL={db_config["url_template"]}')
            depends_on.append(db_config['service_name'])

        config = {
            'build': {
                'context': './backend',
                'dockerfile': 'Dockerfile'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-backend',
            'ports': ['3000'],
            'environment': environment,
            'volumes': ['./backend:/app'],
            'networks': ['app-network']
        }

        if depends_on:
            config['depends_on'] = depends_on

        return config

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

        db_config = detect_database_service(components)
        dependencies = {
            "express": "^4.18.2"
        }
        if db_config and 'express' in db_config['req']:
            dependencies[db_config['req']['express']] = "*"

        package_json = {
            "name": "express-app",
            "version": "1.0.0",
            "main": "server.js",
            "scripts": {
                "start": "node server.js"
            },
            "dependencies": dependencies
        }

        return {
            'package.json': json.dumps(package_json, indent=2),
            'server.js': '''const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Express!');
});

app.listen(port, () => {
  console.log(`Express app listening at http://localhost:${port}`);
});
'''
        }