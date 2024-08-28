import requests

from collections.abc import Mapping
from typing import Any, Dict, Generic, List, Optional, TypeVar

from .api import (
    API, 
    URL,
)

T = TypeVar("T")

class ProjectController(Generic[T]):
    def get_project(name: str) -> Dict[str, Any]:
        response = API._get(url=URL.project(name=name))
        return response
    
    def get_assigned_projects(self):
        response = API._get(url=URL.assigned_projects)
        return response
    
    def get_assets(self) -> None:
        response = API._get(url=URL.all_assets)
        return response
        
    def get_all_shots(self) -> None:
        print("getting shots")

    def get_shots_by_episode(
        self,
        episode: int,
        expand: Optional[List[str]] = [],
    ) -> None:
        response = API._get(url=URL.shots_by_episode(episode=episode))
        return response