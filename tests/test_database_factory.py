import unittest
from mkdf.templates.factories.database_factory import DatabaseFactory
from mkdf.templates.docker.services.databases.postgresql import PostgreSQLService
from mkdf.templates.docker.services.databases.mysql import MySQLService
from mkdf.templates.docker.services.databases.mariadb import MariaDBService
from mkdf.templates.docker.services.databases.mongodb import MongoDBService

class TestDatabaseFactory(unittest.TestCase):

    def setUp(self):
        self.factory = DatabaseFactory()

    def test_get_postgresql_service(self):
        service = self.factory.get_service('postgresql')
        self.assertIsInstance(service, PostgreSQLService)

    def test_get_mysql_service(self):
        service = self.factory.get_service('mysql')
        self.assertIsInstance(service, MySQLService)

    def test_get_mariadb_service(self):
        service = self.factory.get_service('mariadb')
        self.assertIsInstance(service, MariaDBService)

    def test_get_mongodb_service(self):
        service = self.factory.get_service('mongodb')
        self.assertIsInstance(service, MongoDBService)

    def test_get_unknown_service(self):
        with self.assertRaises(ValueError):
            self.factory.get_service('unknown')

if __name__ == '__main__':
    unittest.main()
