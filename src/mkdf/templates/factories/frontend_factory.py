from typing import Dict, Any, List, Optional

from mkdf.templates.docker.base.service_template import DockerService
from mkdf.templates.docker.services.frontends.vue import VueService
from mkdf.templates.docker.services.frontends.react import ReactService
from mkdf.templates.docker.services.frontends.angular import AngularService
from mkdf.templates.docker.services.frontends.svelte import SvelteService
from mkdf.templates.docker.services.frontends.nextjs import NextJSService
from mkdf.templates.docker.services.frontends.nuxtjs import NuxtJSService


class FrontendFactory:
    def __init__(self):
        self._creators = {
            "vue": VueService,
            "react": ReactService,
            "angular": AngularService,
            "svelte": SvelteService,
            "nextjs": NextJSService,
            "nuxtjs": NuxtJSService,
        }

    def get_service(self, frontend_type: str) -> DockerService:
        creator = self._creators.get(frontend_type)
        if not creator:
            raise ValueError(f"Unknown frontend service: {frontend_type}")
        return creator()
