from typing import Dict, Any, List, Optional

from mkdf.templates.docker.base.service_template import DockerService
from mkdf.templates.docker.services.infrastructure.nginx import NginxService
from mkdf.templates.docker.services.infrastructure.traefik import TraefikService
from mkdf.templates.docker.services.infrastructure.monitoring import MonitoringService
from mkdf.templates.docker.services.infrastructure.redis import RedisService
from mkdf.templates.docker.services.infrastructure.celery import CeleryService
from mkdf.templates.docker.services.infrastructure.prometheus import PrometheusService
from mkdf.templates.docker.services.infrastructure.grafana import GrafanaService
from mkdf.templates.docker.services.infrastructure.rabbitmq import RabbitMQService
from mkdf.templates.docker.services.infrastructure.loki import LokiService
from mkdf.templates.docker.services.infrastructure.promtail import PromtailService


class InfrastructureFactory:
    def __init__(self):
        self._creators = {
            "nginx": NginxService,
            "traefik": TraefikService,
            "redis": RedisService,
            "celery": CeleryService,
            "rabbitmq": RabbitMQService,
            "prometheus": PrometheusService,
            "grafana": GrafanaService,
            "loki": LokiService,
            "promtail": PromtailService,
            "monitoring": MonitoringService, # Composite service
        }

    def get_service(self, infra_type: str) -> DockerService:
        creator = self._creators.get(infra_type)
        if not creator:
            raise ValueError(f"Unknown infrastructure service: {infra_type}")
        return creator()
