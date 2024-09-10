from pydantic_core import Url
import requests

from collections.abc import Mapping
from typing import Any, Dict, Generic, List, Optional, TypeVar

from lemonsky.common.models import BaseModel
from lemonsky.data.dashboard.models import (
    ProjectModel,
    AssetModel,
    ShotModel,
    MotionModel,
    TaskModel,
    VersionModel,
    FileModel,
    ContentState,
    ContentType,
)
from .url_wrapper import (
    APIConfig,
    URL,
)

_api =  APIConfig()
T = TypeVar("T")
ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseController(Generic[ModelT]):
    model: type[ModelT]

class Project(BaseController[ProjectModel]):
    model = ProjectModel

    @classmethod
    def get(cls, code: str) -> ProjectModel:
        result = _api._get(url=URL.project(code=code))[0]
        project = cls.model.from_dict(result)
        return project

    @classmethod
    def get_assigned_projects(cls):
        projects = _api._get(url=URL.assigned_projects)
        return projects

class Shot(BaseController[ShotModel]):
    model = ShotModel
    @classmethod
    def get(
        cls, 
        name: str,
        project_code: str
    ) -> ShotModel:
        assert project_code, "Must pass in project code. "
        project = Project.get(code=project_code)
        result = _api._get(
            url=URL.get_shot(
                shot_code=name, 
                project_id=project.id
            )
        )[0]
        shot = cls.model.from_dict(result)
        return shot
        

class Asset(BaseController[AssetModel]):
    model = AssetModel


class Motion(BaseController[MotionModel]):
    model = MotionModel


class Content():
    @classmethod
    def get(
        cls,
        project_code: str,
        type: ContentType,
        name: str,
    ):
        CONTENT_CLASS_MAP = {
            "shot": Shot,
            "asset": Asset,
            "motion": Motion,
        }
        content_class = CONTENT_CLASS_MAP[type]
        result = content_class.get(name=name, project_code=project_code)
        content = cls.model.from_dict(result)
        return content

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
