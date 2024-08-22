import inspect
import requests

from dataclasses import Field, asdict, dataclass, fields
from typing import Any, Dict, List

from .api import API

@dataclass
class BaseController:
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
        params = inspect.signature(cls).parameters

        return cls(
            **{
                k: v for k, v in dict_.items()
                if k in params
            }
        )


class Project(BaseController):
    def __init__(self):
        self.api = API()
    def get_all_projects(self):
        url = f"{self.api.host}{self.api.api_version}dashboard/projects/"
        print("get all projects")
        response = requests.get(url=url)
    
    def get_assets(self):
        print("getting assets")
        
        
    def get_shots(self):
        print("getting shots")
