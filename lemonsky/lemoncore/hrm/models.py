from dataclasses import dataclass

from lemonsky.common.models import BaseModel


@dataclass
class EmployeeModel(BaseModel):
    id: int
    name: str
    url: str