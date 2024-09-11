import inspect

from dataclasses import asdict, dataclass
from typing import Annotated, Any, Dict, TypeVar

from pydantic import Field


_UnionT = TypeVar("_UnionT")
LeftToRight = Annotated[
    _UnionT,
    Field(union_mode="left_to_right"),
]

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
        assert type(dict_) != list, f"{cls.__name__} instance must not be a List. "
        params = inspect.signature(cls).parameters
        _ = {
            k: v for k, v in dict_.items()
            if k in params
        }

        return cls(**_)


@dataclass
class SelfURLModel(BaseModel):
    id: int
    url: str
