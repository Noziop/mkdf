import unittest
from mkdf.templates.factories.frontend_factory import FrontendFactory
from mkdf.templates.docker.services.frontends.vue import VueService
from mkdf.templates.docker.services.frontends.react import ReactService
from mkdf.templates.docker.services.frontends.angular import AngularService

class TestFrontendFactory(unittest.TestCase):

    def setUp(self):
        self.factory = FrontendFactory()

    def test_get_vue_service(self):
        service = self.factory.get_service('vue')
        self.assertIsInstance(service, VueService)

    def test_get_react_service(self):
        service = self.factory.get_service('react')
        self.assertIsInstance(service, ReactService)

    def test_get_angular_service(self):
        service = self.factory.get_service('angular')
        self.assertIsInstance(service, AngularService)

    def test_get_unknown_service(self):
        with self.assertRaises(ValueError):
            self.factory.get_service('unknown')

if __name__ == '__main__':
    unittest.main()
