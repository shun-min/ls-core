from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict

from .enums import (
    ContentType,
    ProjectDivision,
    ProjectStage,
    ProjectType,
)
from lemonsky.common.models import (
    BaseModel, 
    LeftToRight, 
    SelfURLModel,
)
from lemonsky.data.hrm.models import (
    ClientModel, 
    EmployeeModel
)


@dataclass
class ProjectModel(BaseModel):
    id: int
    code: str
    full_name: str
    is_secret: bool
    shotgun_project_id: int | None
    production_path: str
    division: ProjectDivision
    stage: ProjectStage
    type: ProjectType
    publish_path: str | None
    version_path: str | None
    workfiles_path: str | None
    poster: str | None
    description: str
    client: LeftToRight[ClientModel | SelfURLModel] | None
    production_path: str
    backup_path: str | None
    project_file_prefix: str | None
    start_date: date
    end_date: date
    creation_date: datetime
    modified_date: datetime
    created_by: LeftToRight[EmployeeModel | SelfURLModel]
    init_file_path: str | None
    working_file_path: str | None


@dataclass
class ContentMixin:
    id: int
    created_dt: datetime
    modified_dt: datetime
    flow_id: int | None
    flow_type: str | None
    project: LeftToRight[ProjectModel | SelfURLModel]
    name: str
    description: str
    outsource: bool
    created_by: LeftToRight[EmployeeModel | SelfURLModel]
    modified_by: LeftToRight[EmployeeModel | SelfURLModel]
    locked_by: LeftToRight[EmployeeModel | SelfURLModel] | None


@dataclass
class ContentGroup:
    id: int
    content: ContentType
    category: str
    type: str


@dataclass
class SeasonModel(ContentMixin, BaseModel):
    name: str


@dataclass
class EpisodeModel(ContentMixin, BaseModel):
    season: SeasonModel


@dataclass
class SequenceModel(ContentMixin, BaseModel):
    episode: EpisodeModel | None

@dataclass
class ShotModel(BaseModel):
    sequence: SequenceModel
    group: ContentGroup


@dataclass
class AssetModel:
    id: int
    shot: ShotModel | None
    slot: int | None
    group: ContentGroup
    initials: str
    batch: str | None


@dataclass
class StepModel(BaseModel):
    id: int
    name: str


@dataclass
class TaskModel(BaseModel):
    id: int
    name: str
    step: StepModel
