from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .__init__ import EmployeeBase, EmployeeCreate, EmployeeUpdate, UserBase
from dependency import get_current_user_from_token

from app.db.dals import EmployeeDAL
from app.db.session import get_db

employee_router = APIRouter()

@employee_router.post("/", response_model=EmployeeBase)
async def create_employee(employee: EmployeeCreate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    employee_dal = EmployeeDAL(db)
    new_employee = await employee_dal.create(
        surname=employee.surname,
        name=employee.name,
        lastname=employee.lastname,
        job_title=employee.job_title,
        salary=employee.salary
    )
    return new_employee

@employee_router.get("/{employee_id}", response_model=EmployeeBase)
async def read_employee(employee_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    employee_dal = EmployeeDAL(db)
    employee = await employee_dal.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@employee_router.get("/", response_model=list[EmployeeBase])
async def read_employees(current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    employee_dal = EmployeeDAL(db)
    employees = await employee_dal.get_all()
    return employees

@employee_router.put("/{employee_id}", response_model=EmployeeBase)
async def update_employee(employee_id: int, employee: EmployeeUpdate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    employee_dal = EmployeeDAL(db)
    updated_employee = await employee_dal.update(
        employee_id,
        surname=employee.surname,
        name=employee.name,
        lastname=employee.lastname,
        job_title=employee.job_title,
        salary=employee.salary
    )
    if updated_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

@employee_router.delete("/{employee_id}")
async def delete_employee(employee_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    employee_dal = EmployeeDAL(db)
    deleted_employee = await employee_dal.delete(employee_id)
    if deleted_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Employee deleted successfully"}