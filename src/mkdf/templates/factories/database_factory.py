from typing import Dict, Any, List, Optional

from mkdf.templates.docker.base.service_template import DockerService
from mkdf.templates.docker.services.databases.postgresql import PostgreSQLService
from mkdf.templates.docker.services.databases.mysql import MySQLService
from mkdf.templates.docker.services.databases.mariadb import MariaDBService
from mkdf.templates.docker.services.databases.mongodb import MongoDBService


class DatabaseFactory:
    def __init__(self):
        self._creators = {
            "postgresql": PostgreSQLService,
            "mysql": MySQLService,
            "mariadb": MariaDBService,
            "mongodb": MongoDBService,
        }

    def get_service(self, db_type: str) -> DockerService:
        creator = self._creators.get(db_type)
        if not creator:
            raise ValueError(f"Unknown database service: {db_type}")
        return creator()
