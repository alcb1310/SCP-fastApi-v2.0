from typing import Optional

from pydantic import BaseModel, EmailStr


class CompanyBase(BaseModel):
    ruc: str
    name: str
    employees: int


class CompanyResponse(CompanyBase):
    uuid: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserPost(UserCreate):
    company_id: str


class CompanyCreate(UserCreate, CompanyBase):
    username: str


class UserResponse(UserBase):
    # company_id: str
    uuid: str

    company: CompanyResponse

    class Config:
        orm_mode = True


class UserChild(UserBase):
    uuid: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_uuid: str
    company_uuid: str


class ProjectBase(BaseModel):
    name: str


class ProjectResponse(ProjectBase):
    uuid: str

    user: UserChild
    company: CompanyResponse

    class Config:
        orm_mode = True


class SupplierUpdate(BaseModel):
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class SupplierBase(SupplierUpdate):
    supplier_id: str
    name: str
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class SupplierResponse(SupplierBase):
    uuid: str

    user: UserChild
    company: CompanyResponse

    class Config:
        orm_mode = True


class BudgetItemBase(BaseModel):
    code: str
    name: str
    accumulates: bool
    level: Optional[int] = None
    parent_id: Optional[str] = None


class BudgetItemResponse(BudgetItemBase):
    uuid: str

    user: UserChild
    company: CompanyResponse
    parent: Optional[BudgetItemBase] = None

    class Config:
        orm_mode = True
