import unittest
from mkdf.templates.factories.infrastructure_factory import InfrastructureFactory
from mkdf.templates.docker.services.infrastructure.nginx import NginxService
from mkdf.templates.docker.services.infrastructure.traefik import TraefikService
from mkdf.templates.docker.services.infrastructure.monitoring import MonitoringService
from mkdf.templates.docker.services.infrastructure.redis import RedisService
from mkdf.templates.docker.services.infrastructure.celery import CeleryService
from mkdf.templates.docker.services.infrastructure.prometheus import PrometheusService
from mkdf.templates.docker.services.infrastructure.grafana import GrafanaService

class TestInfrastructureFactory(unittest.TestCase):

    def setUp(self):
        self.factory = InfrastructureFactory()

    def test_get_nginx_service(self):
        service = self.factory.get_service('nginx')
        self.assertIsInstance(service, NginxService)

    def test_get_traefik_service(self):
        service = self.factory.get_service('traefik')
        self.assertIsInstance(service, TraefikService)

    def test_get_redis_service(self):
        service = self.factory.get_service('redis')
        self.assertIsInstance(service, RedisService)

    def test_get_celery_service(self):
        service = self.factory.get_service('celery')
        self.assertIsInstance(service, CeleryService)

    def test_get_prometheus_service(self):
        service = self.factory.get_service('prometheus')
        self.assertIsInstance(service, PrometheusService)

    def test_get_grafana_service(self):
        service = self.factory.get_service('grafana')
        self.assertIsInstance(service, GrafanaService)

    def test_get_monitoring_service(self):
        service = self.factory.get_service('monitoring')
        self.assertIsInstance(service, MonitoringService)

    def test_get_unknown_service(self):
        with self.assertRaises(ValueError):
            self.factory.get_service('unknown')

if __name__ == '__main__':
    unittest.main()
