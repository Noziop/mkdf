
import unittest
from mkdf.templates.factories.docker_factory import DockerComposeFactory

class TestEnvGeneration(unittest.TestCase):

    def test_mariadb_env(self):
        components = ['fastapi', 'mariadb']
        project_name = 'test-project'
        project_structure = DockerComposeFactory.create(components, project_name)
        env_content = project_structure['.env']
        self.assertIn('PROJECT_NAME=test-project', env_content)
        self.assertIn('MARIADB_ROOT_PASSWORD=rootpassword', env_content)
        self.assertIn('MARIADB_DATABASE=dbname', env_content)
        self.assertIn('MARIADB_USER=user', env_content)
        self.assertIn('MARIADB_PASSWORD=password', env_content)
        self.assertIn('SECRET_KEY=your-super-secret-key-here', env_content)
        self.assertIn('DEBUG=true', env_content)
        self.assertNotIn('POSTGRES_USER', env_content)
        self.assertNotIn('MYSQL_ROOT_PASSWORD', env_content)

    def test_postgresql_env(self):
        components = ['django', 'postgresql']
        project_name = 'test-project'
        project_structure = DockerComposeFactory.create(components, project_name)
        env_content = project_structure['.env']
        self.assertIn('PROJECT_NAME=test-project', env_content)
        self.assertIn('POSTGRES_USER=user', env_content)
        self.assertIn('POSTGRES_PASSWORD=password', env_content)
        self.assertIn('POSTGRES_DB=dbname', env_content)
        self.assertIn('SECRET_KEY=your-super-secret-key-here', env_content)
        self.assertIn('DEBUG=true', env_content)
        self.assertNotIn('MARIADB_ROOT_PASSWORD', env_content)
        self.assertNotIn('MYSQL_ROOT_PASSWORD', env_content)

    def test_mysql_env(self):
        components = ['flask', 'mysql']
        project_name = 'test-project'
        project_structure = DockerComposeFactory.create(components, project_name)
        env_content = project_structure['.env']
        self.assertIn('PROJECT_NAME=test-project', env_content)
        self.assertIn('MYSQL_ROOT_PASSWORD=rootpassword', env_content)
        self.assertIn('MYSQL_DATABASE=dbname', env_content)
        self.assertIn('MYSQL_USER=user', env_content)
        self.assertIn('MYSQL_PASSWORD=password', env_content)
        self.assertIn('SECRET_KEY=your-super-secret-key-here', env_content)
        self.assertIn('DEBUG=true', env_content)
        self.assertNotIn('POSTGRES_USER', env_content)
        self.assertNotIn('MARIADB_ROOT_PASSWORD', env_content)

    def test_mongodb_env(self):
        components = ['express', 'mongodb']
        project_name = 'test-project'
        project_structure = DockerComposeFactory.create(components, project_name)
        env_content = project_structure['.env']
        self.assertIn('PROJECT_NAME=test-project', env_content)
        self.assertIn('MONGO_INITDB_ROOT_USERNAME=user', env_content)
        self.assertIn('MONGO_INITDB_ROOT_PASSWORD=password', env_content)
        self.assertIn('MONGO_INITDB_DATABASE=dbname', env_content)
        self.assertIn('SECRET_KEY=your-super-secret-key-here', env_content)
        self.assertIn('DEBUG=true', env_content)
        self.assertNotIn('POSTGRES_USER', env_content)
        self.assertNotIn('MYSQL_ROOT_PASSWORD', env_content)
        self.assertNotIn('MARIADB_ROOT_PASSWORD', env_content)

if __name__ == '__main__':
    unittest.main()
