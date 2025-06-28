from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class FlaskService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        db_config = detect_database_service(components)
        environment = []
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
            'ports': ['5000'],
            'environment': environment,
            'volumes': ['./backend:/app'],
            'networks': ['app-network']
        }

        if depends_on:
            config['depends_on'] = depends_on

        return config

    def get_dockerfile_content(self):
        return '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
'''

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        if components is None:
            components = []

        requirements = ['Flask==3.0.0', 'Flask-Cors==4.0.0']
        db_config = detect_database_service(components)
        if db_config:
            requirements.append(db_config['req']['flask'])

        return {
            'app.py': '''from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, from Flask!'

@app.route('/api/v1/health')
def health_check():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        return jsonify({"status": "healthy", "database_url": db_url})
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
''',
            'requirements.txt': '\n'.join(requirements)
        }