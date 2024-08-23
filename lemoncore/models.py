from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict


class BaseModel:
    '''
    Base class to be implemented by concrete controllers
    
    '''
    def to_dict(self) -> Dict[str, Any]:
        dict_ = {
            k: v for k, v in asdict(self).items()
        }
        return dict_

    @classmethod
    def from_dict(cls, dict_: dict):
        _ = {
            k: v for k, v in dict_.items()
            if k in cls.__annotations__
        }
        
        return cls(**_)


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
    # created_by: LeftToRight[EmployeeModel | SelfURLModel]
    init_file_path: str | None
    working_file_path: str | None


@dataclass
class ContentMixin:
    id: int
    created_dt: datetime
    modified_dt: datetime
    flow_id: int | None
    flow_type: str | None
    # project: LeftToRight[ProjectModel | SelfURLModel]
    name: str
    description: str
    outsource: bool
    # created_by: LeftToRight[EmployeeModel | SelfURLModel]
    # modified_by: LeftToRight[EmployeeModel | SelfURLModel]
    # locked_by: LeftToRight[EmployeeModel | SelfURLModel] | None
    

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