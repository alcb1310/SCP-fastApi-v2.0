import uuid

from pydantic import BaseModel, EmailStr


class CompanyBase(BaseModel):
    ruc: str
    name: str
    employees: int


class CompanyResponse(CompanyBase):
    uuid: uuid.UUID

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    uuid: uuid.UUID

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_uuid: uuid.UUID