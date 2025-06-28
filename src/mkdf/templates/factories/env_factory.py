from typing import List, Optional

from mkdf.templates.docker.base.db_utils import detect_database_service


class EnvFactory:
    DOCKER_COMPONENT_CATEGORIES = {
        "Backend": ["fastapi", "flask", "express", "gofiber", "laravel", "django", "symfony"],
        "Frontend": ["vue", "react", "svelte", "angular", "nextjs", "nuxtjs"],
        "Fullstack": ["laravel", "django", "symfony"],
        "Database": ["postgresql", "mysql", "mariadb", "mongodb"],
        "Cache/Queue": ["redis", "celery", "rabbitmq"],
        "Proxy": ["nginx", "traefik"],
        "Monitoring": ["prometheus", "grafana"]
    }

    @staticmethod
    def generate(components: List[str], project_name: str) -> str:
        env_vars = [f'PROJECT_NAME={project_name}']
        db_config = detect_database_service(components)
        if db_config:
            env_vars.extend(db_config['env_vars'])

        backend_type = next((c for c in components if c in EnvFactory.DOCKER_COMPONENT_CATEGORIES["Backend"]), None)
        if backend_type:
            env_vars.extend(['SECRET_KEY=your-super-secret-key-here', 'DEBUG=true'])

        return "\n".join(env_vars)

