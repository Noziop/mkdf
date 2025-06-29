import unittest
from mkdf.templates.factories.docker_factory import DockerComposeFactory

class TestDockerGeneration(unittest.TestCase):

    def test_fastapi_mariadb_combo(self):
        components = ['fastapi', 'mariadb']
        project_name = 'test-project'
        project_structure = DockerComposeFactory.create(components, project_name)

        # Verify .env file
        self.assertIn('.env', project_structure)
        env_content = project_structure['.env']
        self.assertIn('PROJECT_NAME=test-project', env_content)
        self.assertIn('MARIADB_ROOT_PASSWORD=rootpassword', env_content)
        self.assertIn('MARIADB_DATABASE=dbname', env_content)
        self.assertIn('MARIADB_USER=user', env_content)
        self.assertIn('MARIADB_PASSWORD=password', env_content)
        self.assertIn('SECRET_KEY=your-super-secret-key-here', env_content)
        self.assertNotIn('POSTGRES_USER', env_content)
        self.assertNotIn('MYSQL_ROOT_PASSWORD', env_content)

        # Verify docker-compose.yml
        self.assertIn('docker-compose.yml', project_structure)
        compose_content = project_structure['docker-compose.yml']
        self.assertIn('services:', compose_content)
        self.assertIn('fastapi:', compose_content)
        self.assertIn('depends_on:\n      - mariadb', compose_content)
        self.assertIn('DATABASE_URL=mysql+pymysql://${MARIADB_USER}:${MARIADB_PASSWORD}@mariadb:3306/${MARIADB_DATABASE}', compose_content)

        # Verify backend config
        self.assertIn('backend', project_structure)
        self.assertIn('app', project_structure['backend'])
        self.assertIn('core', project_structure['backend']['app'])
        self.assertIn('config.py', project_structure['backend']['app']['core'])
        config_content = project_structure['backend']['app']['core']['config.py']
        self.assertIn('DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://${MARIADB_USER}:${MARIADB_PASSWORD}@mariadb:3306/${MARIADB_DATABASE}")', config_content)

    def test_django_postgres_combo(self):
        components = ['django', 'postgresql']
        project_name = 'django-project'
        project_structure = DockerComposeFactory.create(components, project_name)

        # Verify .env file
        self.assertIn('.env', project_structure)
        env_content = project_structure['.env']
        self.assertIn('PROJECT_NAME=django-project', env_content)
        self.assertIn('POSTGRES_USER=user', env_content)
        self.assertIn('POSTGRES_PASSWORD=password', env_content)
        self.assertIn('POSTGRES_DB=dbname', env_content)
        self.assertNotIn('MARIADB_ROOT_PASSWORD', env_content)

        # Verify docker-compose.yml
        self.assertIn('docker-compose.yml', project_structure)
        compose_content = project_structure['docker-compose.yml']
        self.assertIn('services:', compose_content)
        self.assertIn('django:', compose_content)
        self.assertIn('depends_on:\n      - postgresql', compose_content)

        # Verify backend config
        self.assertIn('backend', project_structure)
        self.assertIn('myproject', project_structure['backend'])
        self.assertIn('settings.py', project_structure['backend']['myproject'])
        settings_content = project_structure['backend']['myproject']['settings.py']
        self.assertIn('django.db.backends.postgresql', settings_content)

if __name__ == '__main__':
    unittest.main()
