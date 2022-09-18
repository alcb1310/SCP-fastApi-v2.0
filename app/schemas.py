import uuid
from datetime import datetime

from pydantic import BaseModel


class CompanyBase(BaseModel):
    ruc: str
    name: str
    employees: int


class CompanyResponse(CompanyBase):
    uuid: uuid.UUID

    class Config:
        orm_mode = True
