from mkdf.templates.factories.backend_factory import BackendFactory
from mkdf.templates.factories.frontend_factory import FrontendFactory
from mkdf.templates.factories.database_factory import DatabaseFactory
from mkdf.templates.factories.infrastructure_factory import InfrastructureFactory

SERVICE_REGISTRY = {
    **{name: creator for name, creator in BackendFactory()._creators.items()},
    **{name: creator for name, creator in FrontendFactory()._creators.items()},
    **{name: creator for name, creator in DatabaseFactory()._creators.items()},
    **{name: creator for name, creator in InfrastructureFactory()._creators.items()},
}

def get_service(service_name: str):
    service_class = SERVICE_REGISTRY.get(service_name)
    
    if not service_class:
        raise ValueError(f"Unknown service: {service_name}")
    return service_class()