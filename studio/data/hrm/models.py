from dataclasses import dataclass
from typing import Union

from studio.common.models import BaseModel


@dataclass
class ClientModel():
    id: int
    name: str
    phone: Union[str, None]
    address: Union[str, None]
    email: Union[str, None]
    slug: str


@dataclass
class DepartmentModel():
    id: int
    department: str


@dataclass
class EmployeeModel(BaseModel):
    id: int
    name: str
    url: str
