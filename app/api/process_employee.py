from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .__init__ import  ProcessEmployeeBase, ProcessEmployeeCreate, ProcessEmployeeUpdate, EmployeeBase, UserBase
from dependency import get_current_user_from_token
from typing import List

from app.db.dals import ProccessEmployeeDAL
from app.db.session import get_db

process_employees_router = APIRouter()

@process_employees_router.post("/", response_model=List[ProcessEmployeeBase])
async def create_process_employee(process_employee: ProcessEmployeeCreate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = ProccessEmployeeDAL(db)
    new_process_employees = await dal.create(proccess_id=process_employee.proccess_id, employee_ids=process_employee.employee_ids)
    new_process_employees = await dal.get_by_process_id(process_employee.proccess_id)
    new_process_employees = [
        ProcessEmployeeBase(
            id=pe.id,
            proccess_id=pe.proccess_id,
            employee_id=pe.employee_id,
            employee=EmployeeBase(
                id=pe.employee.id,
                surname=pe.employee.surname,
                name=pe.employee.name,
                lastname=pe.employee.lastname,
                job_title=pe.employee.job_title,
                salary=pe.employee.salary,
            )
        ) for pe in new_process_employees
    ]
    return new_process_employees

@process_employees_router.get("/process_employees/{proccess_id}", response_model=List[ProcessEmployeeBase])
async def read_process_employees(proccess_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = ProccessEmployeeDAL(db)
    process_employees = await dal.get_by_process_id(proccess_id)
    process_employees = [
        ProcessEmployeeBase(
            id=pe.id,
            proccess_id=pe.proccess_id,
            employee_id=pe.employee_id,
            employee=EmployeeBase(
                id=pe.employee.id,
                surname=pe.employee.surname,
                name=pe.employee.name,
                lastname=pe.employee.lastname,
                job_title=pe.employee.job_title,
                salary=pe.employee.salary,
            )
        ) for pe in process_employees
    ]
    return process_employees

@process_employees_router.put("/{process_id}", response_model=List[ProcessEmployeeBase])
async def update_process_employees(proccess_emlployee: ProcessEmployeeUpdate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = ProccessEmployeeDAL(db)
    proccess_emlployee_dumped = proccess_emlployee.model_dump()
    await dal.update_by_process_id(**proccess_emlployee_dumped)
    updated_process_employees = await dal.get_by_process_id(proccess_emlployee.proccess_id)
    updated_process_employees = [
        ProcessEmployeeBase(
            id=pe.id,
            proccess_id=pe.proccess_id,
            employee_id=pe.employee_id,
            employee=EmployeeBase(
                id=pe.employee.id,
                surname=pe.employee.surname,
                name=pe.employee.name,
                lastname=pe.employee.lastname,
                job_title=pe.employee.job_title,
                salary=pe.employee.salary,
            )
        ) for pe in updated_process_employees
    ] 
    return updated_process_employees

@process_employees_router.delete("/{proccess_id}/{employee_id}")
async def delete_process_employee(proccess_id: int, employee_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = ProccessEmployeeDAL(db)
    deleted_process_employee = await dal.delete_by_process_and_employee_id(proccess_id, employee_id)
    if deleted_process_employee is None:
        raise HTTPException(status_code=404, detail="ProcessEmployee not found")
    return {"detail": "ProcessEmployee deleted successfully"}