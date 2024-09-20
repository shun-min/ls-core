from datetime import datetime
import os
import requests
import sys

from collections.abc import Mapping
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

import django

from lemonsky.common.models import BaseModel
from lemonsky.data.dashboard.models import (
    ProjectModel,
    AssetModel,
    ShotModel,
    MotionModel,
    StepModel,
    TaskModel,
    VersionModel,
    PreviewVersionModel,
    FileModel,
    ContentState,
    ContentTypeEnums,
)
from .url_wrapper import (
    APIConfig,
    URL,
)

sys.path.append(r"D:\projects\work\LemonCORE-Docker\django\lemoncore")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lemoncore.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from skyline.models import (
    SkylineProject,
    SkylineTask,
    SkylineVersion,
    SkylineVersionPreview,
    PublishKey,
)
from skyline.models import File as SkylineFile
from skylinecontent.models import ContentGroup
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


class Project(BaseController[ProjectModel], ProjectModel):
    model=ProjectModel

    @classmethod
    def get(cls, code: str) -> ProjectModel:
        result = SkylineProject.objects.get(code=code)
        return cls.model.from_django(cls, result)


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
                name=name, 
                project_id=project.id
            )
        )[0]
        return cls.model.from_dict(result)
        

class Shot(BaseController[ShotModel], ShotModel):
    model = ShotModel
    
    @classmethod
    def get(
        cls, 
        project_code: str,
        name: Union[int, str],
    ) -> ShotModel:
        assert project_code, "Must pass in project code. "
        if isinstance(name, int):
            name = str(name)
        result = SkylineShot.objects.get(
            project__code=project_code,
            name=name,
        )
        return cls.model.from_django(cls, result)

    # def get_tasks(self):
    #     shot_code = self.name.split("_")
    #     episode = shot_code[0]
    #     sequence = shot_code[1]
    #     shot = shot_code[2]
        
    #     # shot = SkylineShot.objects.get(
    #     #     project__code=self.project.code, 
    #     #     sequence__episode__name=episode,
    #     #     sequence__name= sequence,
    #     #     name=shot,
    #     # )


class Asset(BaseController[AssetModel]):
    model = AssetModel

    @classmethod
    def get(
        cls,
        name: str,
        group: str,
    ) -> AssetModel:
        initial = name[0]
        content_group = ContentGroup.objects.get(name=group)
        result = SkylineAsset.objects.create(
            name=name,
            initials=initial,
            group=content_group,
        )
        return cls.model.from_django(cls, result)


class Motion(BaseController[MotionModel]):
    model = SkylineMotion


class Content():
    @classmethod
    def get(
        cls,
        type: ContentTypeEnums,
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


class Task(BaseController[TaskModel], TaskModel):
    model = TaskModel
    
    @classmethod
    def get(
        cls,
        project_code: str,
        content_type: str,
        content_name: str,
        step_code: str,
    ) -> TaskModel:  
        CONTENT_CLASS_MAP = {
            "shot": Shot,
            "asset": Asset,
            "motion": Motion,
        }
        
        content_class = CONTENT_CLASS_MAP[content_type]
        c = ContentType.objects.get(model=content_type)
        content = content_class.get(
            project_code=project_code, 
            name=content_name,
        )
        result = SkylineTask.objects.filter(
            project_content_type=c.id,
            project_content_reference_id=content.id,
            step__code=step_code,
        )[0]

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
        client_version: str,
    ):
        return Version.create(task_id=self.id, client_version=client_version)


class Version(BaseController[VersionModel], VersionModel):
    model = VersionModel
        
    @classmethod
    def get(
        cls, 
        internal_version: Optional[int] = None,
        client_version: Optional[int] = None,
        id: Optional[int] = None,
        task: Optional[TaskModel] = None,
    ) -> List[VersionModel]:
        if id:
            result = SkylineVersion.objects.filter(id=id)
        if task and internal_version:
            result = SkylineVersion.objects.filter(
                task__id= task.id,
                task__step__name=task.step.name,
                internal_version=internal_version,
            )
        versions = [
            cls.model.from_django(cls, _)
            for _ in result
        ]
        return versions

    @classmethod
    def create(
        cls, 
        client_version: str,
        task: SkylineTask,
    ) -> VersionModel:
        result = SkylineVersion.objects.create(
            status="wip",
            task=task,
            client_version=2,
            publish_time=datetime.now(),
        )
        return cls.model.from_django(cls, result)
    
    def add_file(
        self,
        file_name: str,
        keys: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        start_frame:  Optional[str] = None,
        end_frame:  Optional[str] = None,
    ) -> bool:
        try:
            result = File.create(
                keys = keys,
                file_name=file_name,
                parent=parent,
                setting_keyword=setting_keyword,
                start_frame=start_frame,
                end_frame=end_frame,
                version=self,
                version_type="skylineversion"
            )
        except Exception as e:
            print(f"File not registered. \n{e}")
            return False
        return True
    
    def get_files(
        self, 
        keys: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
    ):
        result = File.get(
            keys=keys,
            parent=parent,
            setting_keyword=setting_keyword,
            version_id=self.id,
            version_type="publish",  # TODO: handle this
        )
        return result

    def publish(self,):
        return

class PreviewVersion(BaseController[PreviewVersionModel], PreviewVersionModel):
    model = PreviewVersionModel

    @classmethod
    def get():
        return
    

class _File(BaseController[FileModel]):
    model = FileModel
    
    @classmethod
    def get(
        cls,
        keys: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        version_id: Optional[int] = None,
    ) -> Dict[str, Union[str, int, Dict[str, str]]]:
        response = _api._get(url=URL.file(version_id=version_id))
        entities = cls.model.from_dict(response.json())
        return entities


class File(BaseController[FileModel], FileModel):
    model = FileModel

    @classmethod
    def filterFilesWithKeys(cls, keys: List[str]):
        queryset = SkylineFile.objects.all()
        while len(keys) > 0:
            k = PublishKey.objects.get(name=keys[-1])
            queryset = queryset.filter(keys=k.id)
            keys.pop(-1)
        return queryset

    @classmethod
    def get(
        cls,
        keys: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        version_type: Optional[str] = "publish",
        version_id: Optional[int] = None,
    ) -> List[FileModel]:

        results = cls.filterFilesWithKeys(keys)
        files = [cls.model.from_django(cls, r) for r in results]

        return files

    @classmethod
    def create(
        cls,
        file_name: str,
        keys: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        start_frame:  Optional[str] = None,
        end_frame:  Optional[str] = None,
        version_type: Optional[str] = "skylineversion",
        version: Optional[VersionModel] = None,
    ) -> FileModel:
        version_contenttype = ContentType.objects.get(
            app_label="skyline", model=version_type
        )

        key_instances = PublishKey.objects.filter(name__in=keys)
        if key_instances.count() != len(keys):
            raise KeyError(f"{len(keys)} keys given, {key_instances.count()} keys found in DB. confirm the key name being passed in during File creation is correct. ")

        result: SkylineFile = SkylineFile.objects.create(
            file_name=file_name,
            parent=parent,
            setting_keyword=setting_keyword,
            version_type=version_contenttype,
            version_id=version.id,
            start_frame=start_frame,
            end_frame=end_frame,
        )
        result.keys.set(key_instances)
        result.save()
        file = cls.from_django(cls, result)
        return file
