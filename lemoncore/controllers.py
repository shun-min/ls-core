import requests

from collections.abc import Mapping
from typing import Any, Dict, Generic, List, TypeVar

from .api import (
    API, 
    URL,
)

T = TypeVar("T")

class ProjectController(Generic[T]):
    def get_assigned_projects(self):
        response = API._get(url=URL.project)
        return response
    
    def get_assets(self) -> None:
        response = API._get(url=URL.all_assets)
        
    def get_all_shots(self) -> None:
        print("getting shots")

    def get_shots_by_episode(
        self,
        episode: int,
        expand: List[str],
    ) -> None:
        API._get(url=URL.shots_by_episode)        
