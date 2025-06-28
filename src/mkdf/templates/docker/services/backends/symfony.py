from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class SymfonyService(DockerService):
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        if components is None:
            components = []

        db_config = detect_database_service(components)
        depends_on = []
        if db_config:
            depends_on.append(db_config['service_name'])

        config = {
            'build': {
                'context': './backend',
                'dockerfile': 'Dockerfile'
            },
            'container_name': '${PROJECT_NAME:-fullstack}-backend',
            'ports': ['8000'],
            'volumes': ['./backend:/app'],
            'networks': ['app-network']
        }

        if depends_on:
            config['depends_on'] = depends_on

        return config

    def get_dockerfile_content(self) -> Optional[str]:
        return '''FROM php:8.1-fpm-alpine

WORKDIR /app

RUN docker-php-ext-install pdo pdo_mysql

COPY . .

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN composer install

EXPOSE 8000

CMD ["php", "-S", "0.0.0.0:8000", "-t", "public"]
'''

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        if components is None:
            components = []

        db_config = detect_database_service(components)
        
        env_content = '''# .env
# Symfony application parameters
APP_ENV=dev
APP_SECRET=your_secret_key
DATABASE_URL="mysql://db_user:db_password@127.0.0.1:3306/db_name?serverVersion=5.7"

# For Docker
# DATABASE_URL="mysql://db_user:db_password@database_host:3306/db_name?serverVersion=5.7"
'''

        if db_config:
            if db_config['service_name'] == 'postgresql':
                env_content = env_content.replace('DATABASE_URL="mysql://db_user:db_password@127.0.0.1:3306/db_name?serverVersion=5.7"', 'DATABASE_URL="postgresql://user:password@postgresql:5432/dbname?serverVersion=15"')
            elif db_config['service_name'] == 'mariadb':
                env_content = env_content.replace('DATABASE_URL="mysql://db_user:db_password@127.0.0.1:3306/db_name?serverVersion=5.7"', 'DATABASE_URL="mysql://user:password@mariadb:3306/dbname?serverVersion=10.6"')
            elif db_config['service_name'] == 'mysql':
                env_content = env_content.replace('DATABASE_URL="mysql://db_user:db_password@127.0.0.1:3306/db_name?serverVersion=5.7"', 'DATABASE_URL="mysql://user:password@mysql:3306/dbname?serverVersion=8.0"')
            elif db_config['service_name'] == 'mongodb':
                env_content = env_content.replace('DATABASE_URL="mysql://db_user:db_password@127.0.0.1:3306/db_name?serverVersion=5.7"', 'DATABASE_URL="mongodb://user:password@mongodb:27017/dbname"')

        return {
            'composer.json': '''{
    "name": "symfony/skeleton",
    "type": "project",
    "license": "MIT",
    "description": "A minimal Symfony project",
    "require": {
        "php": ">=8.1",
        "symfony/flex": "^2.2",
        "symfony/framework-bundle": "^6.2",
        "symfony/runtime": "^6.2",
        "symfony/yaml": "^6.2"
    }
}
''',
            '.env': env_content
        }