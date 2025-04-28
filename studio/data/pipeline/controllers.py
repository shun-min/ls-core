from datetime import datetime
import os
import requests
import sys

from abc import abstractmethod
from collections.abc import Mapping
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

import django

from studio.common.models import BaseModel
from studio.common.singleton import Singleton
from studio.data.pipeline.models import (
    ProjectModel,
    AssetModel,
    ShotModel,
    MotionModel,
    StepModel,
    TaskModel,
    VersionModel,
    PreviewVersionModel,
    FileModel,
    TagModel,
    ContentState,
    ContentTypeEnums,
)
from .url_wrapper import (
    APIConfig,
    URL,
)

from django.contrib.contenttypes.models import ContentType
from studio.models import (
    StudioProject,
    StudioProjectCrew,
    StudioStep,
    StudioTask,
    StudioVersion,
    StudioVersionPreview,
    Tag,
)
from studio.models import File as _File
from studiocontent.models import (
    ContentGroup,
)
from studiocontent.models import Shot as _Shot
from studiocontent.models import Asset as _Asset
from studiocontent.models import Motion as _Motion


# _api =  APIConfig()


class BaseController():
    """
    Abstract class defining field that holds model type value
    """
    model: type[ModelT]


class Project(BaseController[ProjectModel], ProjectModel):
    model=ProjectModel

    @classmethod
    def get(
        cls, 
        code: Optional[str] = "",
        id: Optional[int] = None,
    ) -> ProjectModel:
        if code:
            result = StudioProject.objects.get(code=code)
        elif id:
            result = StudioProject.objects.get(id=id)
        return cls.model.from_django(cls, result)

    @classmethod
    def get_assigned(
        cls, 
        lsid: str
    ) -> List[ProjectModel]:
        crews = StudioProjectCrew.objects.filter(employee__employee_id=lsid.lower())
        project_ids = [c.project.pk for c in crews]
        result = StudioProject.objects.filter(id__in=project_ids)
        return [cls.model.from_django(cls, p) for p in result]


# class _Shot(BaseController[ShotModel]):
#     model = ShotModel

#     @classmethod
#     def get(
#         cls,
#         name: str,
#         project_code: str
#     ) -> ShotModel:
#         assert project_code, "Must pass in project code. "
#         project = Project.get(code=project_code)
#         result = _api._get(
#             url=URL.get_shot(
#                 name=name,
#                 project_id=project.id
#             )
#         )[0]
#         return cls.model.from_dict(result)


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
        result = _Shot.objects.get(
            project__code=project_code,
            name=name,
        )
        return cls.model.from_django(cls, result)

    @classmethod
    def get_all(
        cls,
        project_code: str,
        category: Optional[str] = None,
    ) -> List[ShotModel]:
        kwargs = {
            "project__code": project_code,
        }
        content_groups = ContentGroup.objects.filter(category=category)
        if category:
            kwargs.update({"group__in": content_groups})
            
        result = _Shot.objects.filter(**kwargs)
        return [cls.model.from_django(cls, r) for r in result]


class Asset(BaseController[AssetModel], AssetModel):
    model = AssetModel

    @classmethod
    def get(
        cls,
        name: str,
        project_code: str,
    ) -> List[AssetModel]:
        assert project_code, "Must pass in project code. "
        kwargs = {
            "name": name,
            "initial": name[0],
            "project_code": project_code,
        }
        result = _Asset.objects.filter(
            **kwargs
        )
        return [cls.model.from_django(cls, r) for r in result]

    @classmethod
    def get_all(
        cls,
        project_code: str,
        category: Optional[List[ContentGroup]] = None,
    ) -> List[AssetModel]:
        kwargs = {
            "project__code": project_code,
        }
        content_groups = ContentGroup.objects.filter(category=category)
        if category:
            kwargs.update({"group__in": content_groups})
        result = _Asset.objects.filter(**kwargs)
        return [cls.model.from_django(cls, r) for r in result]


class Motion(BaseController[MotionModel], MotionModel):
    model = _Motion


class Content():
    CONTENT_CLASS_MAP = {
        "shot": Shot,
        "asset": Asset,
        "motion": Motion,
    }
    @classmethod
    def get(
        cls,
        type: ContentTypeEnums,
        name: str,
        project_code: str,
        category: Optional[str] = None,
    ) -> List[Union[ShotModel, AssetModel, MotionModel]]:
        content_class = cls.CONTENT_CLASS_MAP[type]
        return content_class.get(name=name, project_code=project_code)

    @classmethod
    def get_all(
        cls,
        type: str,
        project_code: str,
        category: Optional[str] = None,
    ) -> List[Union[ShotModel, AssetModel, MotionModel]]:
        content_class = cls.CONTENT_CLASS_MAP[type]
        kwargs = {
            "project_code": project_code,
        }
        if category:
            kwargs.update({"category": category})
            
        return content_class.get_all(**kwargs)


class Step(BaseController[ProjectModel]):
    model = StepModel

    @classmethod
    def get(cls, code: str) -> StepModel:
        result = StudioStep._get(code=code)[0]
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
    ) -> List[TaskModel]:
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
        result = StudioTask.objects.filter(
            project_content_type=c.id,
            project_content_reference_id=content.id,
            step__code=step_code,
        )
        return [cls.model.from_django(cls, t) for t in result]

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
            result = StudioVersion.objects.filter(id=id)
        elif task and internal_version:
            result = StudioVersion.objects.filter(
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
        task: StudioTask,
    ) -> VersionModel:
        result = StudioVersion.objects.create(
            status="wip",
            task=task,
            client_version=2,
            publish_time=datetime.now(),
        )
        return cls.model.from_django(cls, result)

    def add_file(
        self,
        name: str,
        tags: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        start_frame:  Optional[str] = None,
        end_frame:  Optional[str] = None,
    ) -> bool:
        try:
            result = File.create(
                tags = tags,
                name=name,
                parent=parent,
                setting_keyword=setting_keyword,
                start_frame=start_frame,
                end_frame=end_frame,
                version=self,
                version_type="studioversion"
            )
        except Exception as e:
            print(f"File not registered. \n{e}")
            return False
        return True

    def get_files(
        self,
        tags: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
    ):
        result = File.get(
            tags=tags,
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
    def get(
        cls,
        id: int, 
        internal_version: int,
        client_version: int,
        parent: Union[VersionModel, int],
    ):  
        args = {}
        if id:
            args.update()
        StudioVersionPreview.objects.filter()
        return


class File(BaseController[FileModel], FileModel):
    model = FileModel

    @classmethod
    def filterFilesWithTags(cls, tags: List[str]):
        queryset = _File.objects.all()
        while len(tags) > 0:
            k = Tag.objects.get(name=tags[-1])
            queryset = queryset.filter(tags=k.id)
            tags.pop(-1)
        return queryset

    @classmethod
    def get(
        cls,
        tags: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        version_type: Optional[str] = "publish",
        version_id: Optional[int] = None,
    ) -> List[FileModel]:

        results = cls.filterFilesWithTags(tags)
        files = [cls.model.from_django(cls, r) for r in results]

        return files

    @classmethod
    def create(
        cls,
        name: str,
        tags: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        start_frame:  Optional[str] = None,
        end_frame:  Optional[str] = None,
        version_type: Optional[str] = "studioversion",
        version: Optional[VersionModel] = None,
    ) -> FileModel:
        version_contenttype = ContentType.objects.get(
            app_label="studio", model=version_type
        )

        tag_instances = Tag.objects.filter(name__in=tags)
        if tag_instances.count() != len(tags):
            raise KeyError(f"{len(tags)} tags given, {tag_instances.count()} tags found in DB. confirm the key name being passed in during File creation is correct. ")

        result = _File.objects.create(
            name=name,
            parent=parent,
            setting_keyword=setting_keyword,
            version_type=version_contenttype,
            version_id=version.id,
            start_frame=start_frame,
            end_frame=end_frame,
        )
        result.tags.set(tag_instances)
        result.save()
        file = cls.from_django(cls, result)
        return file
