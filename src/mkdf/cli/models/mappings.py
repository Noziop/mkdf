from ...templates.template_factory import TEMPLATE_CATEGORIES
from ...templates.factories.env_factory import EnvFactory

def create_template_mapping():
    template_map = {}
    current_id = 1

    for template in TEMPLATE_CATEGORIES.get("Backend API", []):
        template_map[str(current_id)] = template
        template_map[template] = template
        current_id += 1

    for template in TEMPLATE_CATEGORIES.get("Frontend SPA", []):
        template_map[str(current_id)] = template
        template_map[template] = template
        current_id += 1

    for template in TEMPLATE_CATEGORIES.get("Fullstack", []):
        template_map[str(current_id)] = template
        template_map[template] = template
        current_id += 1

    for template in TEMPLATE_CATEGORIES.get("Static Site", []):
        template_map[str(current_id)] = template
        template_map[template] = template
        current_id += 1

    return template_map

def create_component_mapping():
    """Create mapping for sequential numbers and component names"""
    categories_order = [
        "Backend", "Frontend", "Fullstack", "Database",
        "Cache/Queue", "Proxy", "Monitoring"
    ]
    components_flat = []
    for category in categories_order:
        components = EnvFactory.DOCKER_COMPONENT_CATEGORIES.get(category, [])
        components_flat.extend(components)

    component_map = {}
    for i, component in enumerate(components_flat, 1):
        component_map[str(i)] = component
        component_map[component] = component

    return component_map
