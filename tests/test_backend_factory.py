import unittest
from mkdf.templates.factories.backend_factory import BackendFactory
from mkdf.templates.docker.services.backends.fastapi import FastAPIService
from mkdf.templates.docker.services.backends.flask import FlaskService
from mkdf.templates.docker.services.backends.django import DjangoService

class TestBackendFactory(unittest.TestCase):

    def setUp(self):
        self.factory = BackendFactory()

    def test_get_fastapi_service(self):
        service = self.factory.get_service('fastapi')
        self.assertIsInstance(service, FastAPIService)

    def test_get_flask_service(self):
        service = self.factory.get_service('flask')
        self.assertIsInstance(service, FlaskService)

    def test_get_django_service(self):
        service = self.factory.get_service('django')
        self.assertIsInstance(service, DjangoService)

    def test_get_unknown_service(self):
        with self.assertRaises(ValueError):
            self.factory.get_service('unknown')

if __name__ == '__main__':
    unittest.main()
