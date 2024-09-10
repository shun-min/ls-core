from dataclasses import dataclass

from lemonsky.common.models import BaseModel


@dataclass
class ClientModel():
    id: int
    name: str
    phone: str | None
    address: str | None
    email: str | None
    slug: str


@dataclass
class EmployeeModel(BaseModel):
    id: int
    name: str
    url: str
