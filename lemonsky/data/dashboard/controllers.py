import requests

from collections.abc import Mapping
from typing import Any, Dict, Generic, List, Optional, TypeVar

from lemonsky.common.models import BaseModel
from lemonsky.data.dashboard.models import (
    ProjectModel,
    AssetModel,
    ShotModel,
    TaskModel,
    VersionModel,
)
from .url_wrapper import (
    API, 
    URL,
)

T = TypeVar("T")
ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseController(Generic[ModelT]):
    model: type[ModelT]


class Project(BaseController[ProjectModel]):
    model=ProjectModel
    @classmethod
    def get(cls, name: str) -> Dict[str, Any]:
        response = API._get(url=URL.project(name=name))
        project = cls.model.from_dict(response.json())
        return project

    @classmethod
    def get_assigned_projects(self):
        response = API._get(url=URL.assigned_projects)
        projects = response.json()
        return projects


class Content(BaseController[ShotModel | AssetModel]):
    def get_tasks():
        
        return 
    

class Task(BaseController[TaskModel]):
    def get_versions():
        return

    def get_files():
        return

    def get_publish_keys():
        return