from mkdf.templates.docker.services.backends.fastapi import FastAPIService
from mkdf.templates.docker.services.backends.flask import FlaskService
from mkdf.templates.docker.services.backends.express import ExpressService
from mkdf.templates.docker.services.backends.gofiber import GoFiberService
from mkdf.templates.docker.services.backends.django import DjangoService
from mkdf.templates.docker.services.backends.laravel import LaravelService
from mkdf.templates.docker.services.backends.symfony import SymfonyService

from mkdf.templates.docker.services.frontends.vue import VueService
from mkdf.templates.docker.services.frontends.react import ReactService
from mkdf.templates.docker.services.frontends.angular import AngularService
from mkdf.templates.docker.services.frontends.svelte import SvelteService
from mkdf.templates.docker.services.frontends.nextjs import NextJSService
from mkdf.templates.docker.services.frontends.nuxtjs import NuxtJSService

from mkdf.templates.docker.services.databases.postgresql import PostgreSQLService
from mkdf.templates.docker.services.databases.mysql import MySQLService
from mkdf.templates.docker.services.databases.mongodb import MongoDBService
from mkdf.templates.docker.services.databases.mariadb import MariaDBService

from mkdf.templates.docker.services.infrastructure.nginx import NginxService
from mkdf.templates.docker.services.infrastructure.traefik import TraefikService
from mkdf.templates.docker.services.infrastructure.monitoring import MonitoringService
from mkdf.templates.docker.services.infrastructure.redis import RedisService
from mkdf.templates.docker.services.infrastructure.celery import CeleryService
from mkdf.templates.docker.services.infrastructure.prometheus import PrometheusService
from mkdf.templates.docker.services.infrastructure.grafana import GrafanaService

SERVICE_REGISTRY = {
    'django': DjangoService,
        'express': ExpressService,
        'fastapi': FastAPIService,
        'flask': FlaskService,
        'gofiber': GoFiberService,
        'laravel': LaravelService,
        'symfony': SymfonyService,
        'angular': AngularService,
        'nextjs': NextJSService,
        'nuxtjs': NuxtJSService,
        'react': ReactService,
        'svelte': SvelteService,
        'vue': VueService,
        'mongodb': MongoDBService,
        'mysql': MySQLService,
        'postgresql': PostgreSQLService,
        'mariadb': MariaDBService,

    'nginx': NginxService,
    'traefik': TraefikService,
    'monitoring': MonitoringService,
    'redis': RedisService,
    'celery': CeleryService,
    'prometheus': PrometheusService,
    'grafana': GrafanaService,
}

def get_service(service_name: str):
    service_class = SERVICE_REGISTRY.get(service_name)
    if not service_class:
        raise ValueError(f"Unknown service: {service_name}")
    return service_class()