from dataclasses import asdict
from typing import Any, Dict, TypeVar


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