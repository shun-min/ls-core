from pydantic_core import Url
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
    FileModel,
    ContentState,
    ContentType,
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
    model = ProjectModel

    @classmethod
    def get(cls, name: str) -> ProjectModel:
        response = API._get(url=URL.project(name=name))
        entities = cls.model.from_dict(response.json())
        return entities

    @classmethod
    def get_assigned_projects(self):
        response = API._get(url=URL.assigned_projects)
        projects = response.json()
        return projects


class Content(BaseController[ShotModel | AssetModel]):
    def get_content(
        project: str,
        type: ContentType,
        name: str,
    ):  
        
        return

    def get_tasks():

        return


class Task(BaseController[TaskModel]):
    model = TaskModel

    @classmethod
    def get():
        return
    
    def get_all_versions():
        return

    def get_latest_version():
        return

    def get_version():
        return
    
    def get_files():
        return

    def get_step():
        return


class Version(BaseController[VersionModel]):
    model = VersionModel
    
    def get_master_file(self):
        return

    def get_task_file(self):
        return
    
    def get_internal_file(self):
        return

    def add_files(self, files: List):
        return

    def publish(self,):
        return


class File(BaseController[FileModel]):
    model = FileModel
    @classmethod
    def get(
        cls,
        keys: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        version_id: Optional[int] = None,
    ) -> Dict[str, str | int | Dict[str, str]]:
        response = API._get(url=URL.file(version_id=version_id))
        entities = cls.model.from_dict(response.json())
        return entities
