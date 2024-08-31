from pydantic import BaseModel, EmailStr
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class UserCreate(TunedModel):
    email: EmailStr
    password: str
    name: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None

class UserBase(BaseModel):
    id: int
    email: EmailStr
    password: str
    name: str

class CompanyBase(BaseModel):
    id: int
    name: str

class CompanyCreate(BaseModel):
    name: str

class CompanyUpdate(BaseModel):
    name: Optional[str] = None

class EmployeeBase(BaseModel):
    id: int
    surname: str
    name: str
    lastname: Optional[str] = None
    job_title: Optional[str] = None
    salary: Optional[float] = None

class EmployeeCreate(BaseModel):
    surname: str
    name: str
    lastname: Optional[str] = None
    job_title: Optional[str] = None
    salary: Optional[float] = None

class EmployeeUpdate(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    job_title: Optional[str] = None
    salary: Optional[float] = None

class ProcessBase(BaseModel):
    id: int
    name: str

class ProcessCreate(BaseModel):
    name: str

class ProcessUpdate(BaseModel):
    name: str

class ProcessBase(BaseModel):
    id: int
    name: str

class ProcessCreate(BaseModel):
    name: str

class ProcessUpdate(BaseModel):
    name: Optional[str] = None

class EmployeeBase(BaseModel):
    id: int
    surname: str
    name: str
    lastname: Optional[str] = None
    job_title: Optional[str] = None
    salary: Optional[float] = None

class ProcessEmployeeBase(BaseModel):
    id: int
    proccess_id: int
    employee_id: int
    employee: EmployeeBase

class ProcessEmployeeCreate(BaseModel):
    proccess_id: int
    employee_ids: List[int]

class ProcessEmployeeUpdate(BaseModel):
    proccess_id: int
    employee_ids: List[int]

class CompanyUserBase(BaseModel):
    id: int
    company_id: int
    user_id: int

class CompanyUserCreate(TunedModel):
    company_id: int
    user_id: int

class CompanyUserUpdate(BaseModel):
    company_id: Optional[int] = None
    user_id: Optional[int] = None