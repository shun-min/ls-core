from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Union

from .enums import (
    ContentTypeEnums,
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
    DepartmentModel,
    EmployeeModel
)


@dataclass
class ProjectModel(BaseModel):
    id: int
    code: str
    display_name: str
    full_name: str
    is_secret: bool
    shotgun_project_id: Union[int, None]
    production_path: str
    division: ProjectDivision
    stage: ProjectStage
    type: ProjectType
    frame_rate: int
    content_types: List[str]
    publish_path: Union[str, None]
    hierarchy: dict[str, str]
    version_path: Union[str, None]
    workfiles_path: Union[str, None]
    poster: Union[str, None]
    description: str
    client: Union[LeftToRight[Union[ClientModel, SelfURLModel]], None]
    production_path: str
    backup_path: Union[str, None]
    project_file_prefix: Union[str, None]
    start_date: date
    end_date: date
    creation_date: datetime
    modified_date: datetime
    created_by: LeftToRight[Union[EmployeeModel, SelfURLModel]]
    init_file_path: Union[str, None]
    working_file_path: Union[str, None]


@dataclass
class CreateModifiedMixin:
    created_dt: datetime
    modified_dt: datetime


@dataclass
class FlowIdTypeMixin:
    flow_id: Union[int, None]
    flow_type: Union[str, None]


@dataclass
class ContentMixin(CreateModifiedMixin, FlowIdTypeMixin):
    id: int
    project: LeftToRight[Union[ProjectModel, SelfURLModel]]
    name: str
    description: str
    outsource: bool
    created_by: LeftToRight[Union[EmployeeModel, SelfURLModel]]
    modified_by: LeftToRight[Union[EmployeeModel, SelfURLModel]]
    locked_by: Union[LeftToRight[Union[EmployeeModel, SelfURLModel]], None]


@dataclass
class ContentGroupModel:
    id: int
    content: ContentTypeEnums
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
    episode: Union[EpisodeModel, None]


@dataclass
class ShotModel(ContentMixin, BaseModel):
    name: str
    sequence: SequenceModel
    group: ContentGroupModel
    outsource: bool


@dataclass
class AssetModel(ContentMixin, BaseModel):
    id: int
    name: str
    shot: Union[ShotModel, None]
    slot: Union[int, None]
    group: ContentGroupModel
    initials: str
    batch: Union[str, None]


@dataclass
class MotionModel(ContentMixin, BaseModel):
    id: int
    asset: Union[AssetModel, None]
    group: ContentGroupModel
    batch: Union[str, None]
    package: Union[str, None]
    department: Union[str, None]
    typeskin: Union[str, None]
    motion_class: Union[str, None]
    subtype: Union[str, None]
    direction: Union[str, None]
    motion_variant: Union[str, None]
    lod: Union[str, None]


ContentState = ShotModel, AssetModel, MotionModel


@dataclass
class StepModel(BaseModel):
    id: int
    code: str
    name: str
    full_name: str
    description: str
    departments: list[LeftToRight[Union[DepartmentModel, SelfURLModel]]]


@dataclass
class TaskModel(BaseModel, CreateModifiedMixin, FlowIdTypeMixin):
    id: int
    draft: bool
    project_content_type: ContentTypeEnums
    project_content: LeftToRight[Union[Any, SelfURLModel]]
    step: LeftToRight[Union[StepModel, SelfURLModel]]
    status: TaskStatus
    priority: TaskPriority
    description: str
    client_version: int
    created_by: EmployeeModel
    assign_by: Union[EmployeeModel, None]
    assign_to: Union[EmployeeModel, None]
    assign_date: Union[datetime, None]
    start_date: date
    end_date: date
    completion_percent: float
    actual_start_date: Union[datetime, None]
    actual_end_date: Union[datetime, None]
    is_master: bool


@dataclass
class VersionModel(BaseModel, CreateModifiedMixin, FlowIdTypeMixin):
    id: int
    task: TaskModel
    client_version: int
    internal_version: int
    checkout_by: Union[EmployeeModel, None]
    publish_time: Union[datetime, None]
    source_file_path: Union[str, None]
    publish_by: Union[EmployeeModel, None]
    publish_comment: Union[str, None]
    client_feedback: Union[str, None]
    status: TaskStatus


@dataclass
class PublishKey(BaseModel):
    id: int
    name: int


@dataclass
class FileModel(BaseModel, CreateModifiedMixin):
    id: int
    version_id: int
    version_type: str
    file_name: str
    keys: List[PublishKey]
    last_collected: datetime
    parent: List[Any]
    setting_keyword: str
    start_frame: int
    end_frame: int
