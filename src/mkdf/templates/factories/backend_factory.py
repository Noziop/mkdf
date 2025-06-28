from typing import Dict, Any, List, Optional

from mkdf.templates.docker.base.service_template import DockerService
from mkdf.templates.docker.services.backends.fastapi import FastAPIService
from mkdf.templates.docker.services.backends.flask import FlaskService
from mkdf.templates.docker.services.backends.django import DjangoService
from mkdf.templates.docker.services.backends.express import ExpressService
from mkdf.templates.docker.services.backends.gofiber import GoFiberService
from mkdf.templates.docker.services.backends.laravel import LaravelService
from mkdf.templates.docker.services.backends.symfony import SymfonyService


class BackendFactory:
    def __init__(self):
        self._creators = {
            "fastapi": FastAPIService,
            "flask": FlaskService,
            "django": DjangoService,
            "express": ExpressService,
            "gofiber": GoFiberService,
            "laravel": LaravelService,
            "symfony": SymfonyService,
        }

    def get_service(self, backend_type: str) -> DockerService:
        creator = self._creators.get(backend_type)
        if not creator:
            raise ValueError(f"Unknown backend service: {backend_type}")
        return creator()
