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
    StepModel,
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
        result = _api._get(url=URL.get_project(code=code))[0]
        return cls.model.from_dict(result)

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
        return cls.model.from_dict(result)

    def name():
        return
        

class Asset(BaseController[AssetModel]):
    model = AssetModel


class Motion(BaseController[MotionModel]):
    model = MotionModel


class Content():
    @classmethod
    def get(
        cls,
        type: ContentType,
        name: str,
        project_code: str,
    ):
        CONTENT_CLASS_MAP = {
            "shot": Shot,
            "asset": Asset,
            "motion": Motion,
        }
        MODEL_MAP = {
            "shot": ShotModel,
            "asset": AssetModel,
            "motion": MotionModel,
        }
        content_class = CONTENT_CLASS_MAP[type]
        model = MODEL_MAP[type]

        return content_class.get(name=name, project_code=project_code)

    def get_tasks():
        return


class Step(BaseController[ProjectModel]):
    model = StepModel

    @classmethod
    def get(cls, code: str) -> StepModel:
        result = _api._get(url=URL.get_step(code=code))[0]
        return cls.model.from_dict(result)


class Task(BaseController[TaskModel]):
    model = TaskModel

    @classmethod
    def get(
        cls,
        project_code: str,
        content_type: str,
        content_name: str,
        step_code: str,
    ):  
        step = Step.get(code=step_code)
        content = Content.get(
            project_code=project_code,
            type=content_type,
            name=content_name,
        )
        result = _api._get(
            url=URL.get_task(
                content_type=content_type,
                content_id=content.id,
                step_id=step.id,
            )
        )[0]
        return cls.model.from_dict(result)

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
    
    def get(
        self,
        content_name: str,
        content_type: str,
        step_code: str,
    ) -> VersionModel:
        task: TaskModel = Task.get()
        result = _api.get(
            url=URL.get_version(
                
            )
        )
        return

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
        response = _api._get(url=URL.file(version_id=version_id))
        entities = cls.model.from_dict(response.json())
        return entities
