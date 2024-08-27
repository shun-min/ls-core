from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any, Dict, TypeVar

from pydantic import Field

from lemonsky.common.models import BaseModel
from lemonsky.lemoncore.hrm.models import EmployeeModel


_UnionT = TypeVar("_UnionT")
LeftToRight = Annotated[
    _UnionT,
    Field(union_mode="left_to_right"),
]


@dataclass
class SelfURLModel(BaseModel):
    id: int
    url: str


@dataclass
class ProjectModel(BaseModel):
    id: int
    code: str
    full_name: str
    is_secret: bool
    shotgun_project_id: int | None
    production_path: str
    # division: ProjectDivision
    # stage: ProjectStage
    # type: ProjectType
    publish_path: str | None
    version_path: str | None
    workfiles_path: str | None
    poster: str | None
    description: str
    # client: LeftToRight[ClientModel | SelfURLModel] | None
    production_path: str
    backup_path: str | None
    project_file_prefix: str | None
    # start_date: date
    # end_date: date
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
    # group: ContentGroupModel


@dataclass
class StepModel(BaseModel):
    id: int
    name: str


@dataclass
class TaskModel(BaseModel):
    id: int
    name: str
    step: StepModel