from mkdf.templates.factories.backend_factory import BackendFactory
from mkdf.templates.factories.frontend_factory import FrontendFactory
from mkdf.templates.factories.database_factory import DatabaseFactory
from mkdf.templates.factories.infrastructure_factory import InfrastructureFactory

SERVICE_REGISTRY = {
}

def get_service(service_name: str):
    backend_factory = BackendFactory()
    if service_name in backend_factory._creators:
        return backend_factory.get_service(service_name)

    frontend_factory = FrontendFactory()
    if service_name in frontend_factory._creators:
        return frontend_factory.get_service(service_name)

    database_factory = DatabaseFactory()
    if service_name in database_factory._creators:
        return database_factory.get_service(service_name)

    infrastructure_factory = InfrastructureFactory()
    if service_name in infrastructure_factory._creators:
        return infrastructure_factory.get_service(service_name)

    service_class = SERVICE_REGISTRY.get(service_name)
    if not service_class:
        raise ValueError(f"Unknown service: {service_name}")
    return service_class()