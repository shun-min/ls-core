from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List

from .enums import (
    ContentType,
    ProjectDivision,
    ProjectStage,
    ProjectType,
    TaskPriority,
    TaskStatus,
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
class ContentGroupModel:
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
    group: ContentGroupModel


@dataclass
class AssetModel:
    id: int
    shot: ShotModel | None
    slot: int | None
    group: ContentGroupModel
    initials: str
    batch: str | None


@dataclass
class MotionModel:
    id: int
    asset: AssetModel | None
    group: ContentGroupModel
    batch: str | None
    package: str | None
    department: str | None
    typeskin: str | None
    motion_class: str | None
    subtype: str | None
    direction: str | None
    motion_variant: str | None
    lod: str | None


ContentState = ShotModel | AssetModel | MotionModel


@dataclass
class StepModel(BaseModel):
    id: int
    name: str


@dataclass
class TaskModel(BaseModel):
    id: int
    flow_id: int | None
    flow_type: str | None
    draft: bool
    project_content_type: ContentType
    project_content: LeftToRight[ContentState | SelfURLModel]
    step: LeftToRight[StepModel | SelfURLModel]
    status: TaskStatus
    priority: TaskPriority
    description: str
    client_version: int
    created_by: EmployeeModel
    creation_time: datetime
    modified_time: datetime
    assign_to: EmployeeModel | None
    assign_date: datetime | None
    assign_by: EmployeeModel | None
    start_date: date
    end_date: date
    completion_percent: float
    actual_start_date: datetime | None
    actual_end_date: datetime | None
    is_master: bool


@dataclass
class VersionModel(BaseModel):
    id: int
    task: TaskModel
    client_version: int
    internal_version: int
    checkout_by: EmployeeModel | None
    modified_time: datetime | None
    source_file_path: str | None
    publish_by: EmployeeModel | None
    publish_time: datetime | None
    publish_comment: str | None
    creation_time: datetime
    client_feedback: str | None
    status: TaskStatus


@dataclass
class PublishKey(BaseModel):
    id: int
    name: int


@dataclass
class FileModel(BaseModel):
    id: int
    version_id: int
    version_type: str
    keys: List[PublishKey]
    parent: List[Any]
    path: str
    setting_keyword: str
    start_frame: int
    end_frame: int
