from datetime import datetime
import os
import sys
import requests

from collections.abc import Mapping
from pydantic_core import Url
from typing import Any, Dict, Generic, List, Optional, TypeVar

import django

from lemonsky.common.models import BaseModel
from lemonsky.data.dashboard.constants import CONTENT_TYPE_MAP
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

sys.path.append(r"D:\projects\work\LemonCORE-Docker\django\lemoncore")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lemoncore.settings')
django.setup()

from skyline.models import (
    SkylineProject,
    SkylineTask,
    SkylineVersion,
)
from skylinecontent.models import Shot as SkylineShot
from skylinecontent.models import Asset as SkylineAsset
from skylinecontent.models import Motion as SkylineMotion


_api =  APIConfig()
T = TypeVar("T")
ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseController(Generic[ModelT]):
    model: type[ModelT]


class _Project(BaseController[ProjectModel]):
    model = ProjectModel

    @classmethod
    def get(cls, code: str) -> ProjectModel:
        result = _api._get(url=URL.get_project(code=code))[0]
        return cls.model.from_dict(result)

    @classmethod
    def get_assigned_projects(cls):
        projects = _api._get(url=URL.assigned_projects)
        return projects


class Project(BaseController[ProjectModel]):
    model=SkylineProject

    @classmethod
    def get(cls, code: str) -> ProjectModel:
        return SkylineProject.objects.get(code=code)


class _Shot(BaseController[ShotModel]):
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
        

class Shot(BaseController[ShotModel]):
    model = SkylineShot
    
    @classmethod
    def get(
        cls, 
        project_code: str,
        name: str,
    ) -> ShotModel:
        assert project_code, "Must pass in project code. "
        shot_code = name.split("_")
        episode = shot_code[0]
        sequence = shot_code[1]
        shot = shot_code[2]
        result = SkylineShot.objects.get(
            project__code=project_code, 
            sequence__episode__name=episode,
            sequence__name= sequence,
            name=shot,
        )
        return result


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


class _Task(BaseController[TaskModel]):
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


class Task(BaseController[TaskModel]):
    model = TaskModel
    
    @classmethod
    def get(
        cls,
        project_code: str,
        content_type: str,
        content_name: str,
        step_code: str,
    ) -> SkylineTask:  
        CONTENT_CLASS_MAP = {
            "shot": Shot,
            "asset": Asset,
            "motion": Motion,
        }
        
        content_class = CONTENT_CLASS_MAP[content_type]
        content_type_id = CONTENT_TYPE_MAP[content_type]
        content = content_class.get(
            project_code=project_code, 
            name=content_name
        )
        result = SkylineTask.objects.get(
            project_content_type=content_type_id,
            project_content_reference_id=content.id,
            step__code=step_code,
        )

        if not result:
            return []
        return result

    def get_all_versions():
        return

    def get_latest_version():
        return

    def get_version():
        return

    def create_version(
        self,
        task: TaskModel,
    ):
        return Version.create(task_id=task.id)



class Version(BaseController[VersionModel]):
    model = VersionModel
    
    @classmethod
    def get(
        cls, 
        id: Optional[int] = None,
        step_name: Optional[str] = None,
        task: Optional[TaskModel] = None,
    ) -> VersionModel:
        if id:
            return SkylineVersion.objects.get(id=id)
        if task:
            return SkylineVersion.objects.get(
                task__project_content_reference_id= task.id,
                task__step__name=step_name,
            )

    @classmethod
    def create(
        cls, 
        task: SkylineTask,
    ) -> SkylineVersion:
        version = SkylineVersion.objects.create(
            status="wip",
            task=task,
            client_version=2,
            # publish_by=1940,
            publish_time=datetime.now(),
        )
        return version
    
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
