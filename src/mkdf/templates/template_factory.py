from typing import Dict, List, Optional, Union, Any
from .base_templates import get_simple_template, get_low_level_template
from .web_templates import get_react_template, get_vue_template, get_flask_template, get_fastapi_template, get_express_template, get_laravel_template, get_slim_template, get_nextjs_template, get_nuxtjs_template, get_angular_template, get_svelte_template, get_static_template, get_django_template, get_springboot_template, get_aspnet_template, get_gofiber_template, get_echo_template, get_ruby_rails_template
from .factories.docker_factory import DockerComposeFactory, PortConfig, ProjectStructure

TEMPLATE_CATEGORIES = {
"Backend API": ["fastapi", "flask", "express", "gofiber"],
"Frontend SPA": ["vue", "react", "svelte", "angular", "nuxtjs"],
"Fullstack": ["laravel", "django", "symfony", "nextjs"],
"Static Site": ["simple", "static"]
}

class TemplateFactory:
    def __init__(self) -> None:
        self.creators: Dict[str, Any] = {
            'simple': get_simple_template,
            'low_level': get_low_level_template,
            'react': get_react_template,
            'vue': get_vue_template,
            'flask': get_flask_template,
            'fastapi': get_fastapi_template,
            'express': get_express_template,
            'laravel': get_laravel_template,
            'slim': get_slim_template,
            'nextjs': get_nextjs_template,
            'nuxtjs': get_nuxtjs_template,
            'angular': get_angular_template,
            'svelte': get_svelte_template,
            'static': get_static_template,
            'django': get_django_template,
            'springboot': get_springboot_template,
            'aspnet': get_aspnet_template,
            'gofiber': get_gofiber_template,
            'echo': get_echo_template,
            'ruby_rails': get_ruby_rails_template,
            'docker': DockerComposeFactory.create,
        }

    def create_template(self, template_type: str, components: Optional[List[str]] = None, port_config: Optional[PortConfig] = None, project_name: Optional[str] = None) -> ProjectStructure:
        creator = self.creators.get(template_type)
        if not creator:
            raise ValueError(f"Unknown template type: {template_type}")
        if template_type == 'docker':
            return creator(components, project_name=project_name, port_config=port_config)
        return creator()

    def get_all_templates(self) -> Dict[str, List[str]]:
        """Get all available templates categorized by type."""
        
        categorized = {
            "Backend API": [],
            "Frontend SPA": [],
            "Fullstack": [],
            "Static Site": []
        }
        
        for template_name, creator in self.creators.items():
            # Si tes creators ont une propriété 'category' ou 'type'
            if hasattr(creator, 'category'):
                category = creator.category
                if category in categorized:
                    categorized[category].append(template_name)
            else:
                # Fallback : catégorisation par nom
                if template_name in ["fastapi", "flask", "express", "slim", "laravel", "django"]:
                    categorized["Backend API"].append(template_name)
                elif template_name in ["vue", "react", "svelte", "angular", "nextjs", "nuxtjs"]:
                    categorized["Frontend SPA"].append(template_name)
                elif template_name in ["laravel", "django", "nextjs"]:
                    categorized["Fullstack"].append(template_name)
                elif template_name in ["simple", "static", "low_level"]:
                    categorized["Static Site"].append(template_name)
        
        return categorized