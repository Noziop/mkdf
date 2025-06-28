from mkdf.templates.docker.base.service_template import DockerService
from typing import List, Dict, Any, Optional
from mkdf.templates.docker.base.db_utils import detect_database_service

class LaravelService(DockerService):
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
            'ports': ['9000'],
            'volumes': ['./backend:/var/www/html'],
            'networks': ['app-network']
        }

        if depends_on:
            config['depends_on'] = depends_on

        return config

    def get_dockerfile_content(self) -> Optional[str]:
        return '''FROM php:8.1-fpm-alpine

WORKDIR /var/www/html

RUN docker-php-ext-install pdo pdo_mysql

COPY . .

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN composer install

EXPOSE 9000

CMD ["php-fpm"]
'''

    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        if components is None:
            components = []

        db_config = detect_database_service(components)
        
        env_content = '''APP_NAME="Laravel"
APP_ENV=local
APP_KEY=base64:YOUR_APP_KEY_HERE
APP_DEBUG=true
APP_URL=http://localhost

LOG_CHANNEL=stack
LOG_LEVEL=debug

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=

BROADCAST_DRIVER=log
CACHE_DRIVER=file
FILESYSTEM_DISK=local
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
SESSION_LIFETIME=120

MEMCACHED_HOST=127.0.0.1

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

MAIL_MAILER=smtp
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS="hello@example.com"
MAIL_FROM_NAME="${APP_NAME}"

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=
AWS_USE_PATH_STYLE_ENDPOINT=false

PUSHER_APP_ID=
PUSHER_APP_KEY=
PUSHER_APP_SECRET=
PUSHER_APP_CLUSTER=mt1

VITE_APP_NAME="${APP_NAME}"
'''

        if db_config:
            if db_config['service_name'] == 'postgresql':
                env_content = env_content.replace('DB_CONNECTION=mysql', 'DB_CONNECTION=pgsql')
                env_content = env_content.replace('DB_HOST=127.0.0.1', 'DB_HOST=postgresql')
                env_content = env_content.replace('DB_PORT=3306', 'DB_PORT=5432')
                env_content = env_content.replace('DB_DATABASE=laravel', 'DB_DATABASE=${POSTGRES_DB}')
                env_content = env_content.replace('DB_USERNAME=root', 'DB_USERNAME=${POSTGRES_USER}')
                env_content = env_content.replace('DB_PASSWORD=', 'DB_PASSWORD=${POSTGRES_PASSWORD}')
            elif db_config['service_name'] == 'mariadb':
                env_content = env_content.replace('DB_HOST=127.0.0.1', 'DB_HOST=mariadb')
                env_content = env_content.replace('DB_DATABASE=laravel', 'DB_DATABASE=${MARIADB_DATABASE}')
                env_content = env_content.replace('DB_USERNAME=root', 'DB_USERNAME=${MARIADB_USER}')
                env_content = env_content.replace('DB_PASSWORD=', 'DB_PASSWORD=${MARIADB_PASSWORD}')
            elif db_config['service_name'] == 'mysql':
                env_content = env_content.replace('DB_DATABASE=laravel', 'DB_DATABASE=${MYSQL_DATABASE}')
                env_content = env_content.replace('DB_USERNAME=root', 'DB_USERNAME=${MYSQL_USER}')
                env_content = env_content.replace('DB_PASSWORD=', 'DB_PASSWORD=${MYSQL_PASSWORD}')

        return {
            'composer.json': '''{
    "name": "laravel/laravel",
    "type": "project",
    "description": "The Laravel Framework.",
    "keywords": ["framework", "laravel"],
    "license": "MIT",
    "require": {
        "php": "^8.1",
        "guzzlehttp/guzzle": "^7.2",
        "laravel/framework": "^10.0",
        "laravel/sanctum": "^3.2",
        "laravel/tinker": "^2.8"
    }
}
''',
            '.env': env_content
        }