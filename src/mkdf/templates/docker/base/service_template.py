from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class DockerService(ABC):
    @abstractmethod
    def get_service_config(self, components: Optional[List[str]] = None) -> Dict[str, Any]:
        """Returns the configuration for the Docker service."""
        pass

    @abstractmethod
    def get_dockerfile_content(self) -> Optional[str]:
        """Returns the content of the Dockerfile, if any."""
        pass

    @abstractmethod
    def get_files(self, components: Optional[List[str]] = None) -> Dict[str, str]:
        """Returns a dictionary of file paths and their content."""
        pass