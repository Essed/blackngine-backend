from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.models import User, Company, Employee, Proccess, ProccessEmployee, CompanyUser
from typing import List, Optional

class UserDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def create(self, email: str, password: str, name: str = None):
        new_user = User(email=email, password=password, name=name)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update(self, user_id: int, email: str = None, password: str = None, name: str = None):
        user = await self.get(user_id)
        if user:
            if email is not None:
                user.email = email
            if password is not None:
                user.password = password
            if name is not None:
                user.name = name
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def delete(self, user_id: int):
        user = await self.get(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
        return user
    
class CompanyDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, company_id: int):
        result = await self.db.execute(select(Company).where(Company.id == company_id))
        return result.scalars().first()

    async def get_by_name(self, name: str):
        result = await self.db.execute(select(Company).where(Company.name == name))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(Company))
        return result.scalars().all()

    async def create(self, name: str):
        new_company = Company(name=name)
        self.db.add(new_company)
        await self.db.commit()
        await self.db.refresh(new_company)
        return new_company

    async def update(self, company_id: int, name: str = None):
        company = await self.get(company_id)
        if company:
            if name is not None:
                company.name = name
            await self.db.commit()
            await self.db.refresh(company)
        return company

    async def delete(self, company_id: int):
        company = await self.get(company_id)
        if company:
            await self.db.delete(company)
            await self.db.commit()
        return company
    
class EmployeeDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, employee_id: int):
        result = await self.db.execute(select(Employee).where(Employee.id == employee_id))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(Employee))
        return result.scalars().all()

    async def create(self, surname: str, name: str, lastname: str = None, job_title: str = None, salary: float = None):
        new_employee = Employee(surname=surname, name=name, lastname=lastname, job_title=job_title, salary=salary)
        self.db.add(new_employee)
        await self.db.commit()
        await self.db.refresh(new_employee)
        return new_employee

    async def update(self, employee_id: int, surname: str = None, name: str = None, lastname: str = None, job_title: str = None, salary: float = None):
        employee = await self.get(employee_id)
        if employee:
            if surname is not None:
                employee.surname = surname
            if name is not None:
                employee.name = name
            if lastname is not None:
                employee.lastname = lastname
            if job_title is not None:
                employee.job_title = job_title
            if salary is not None:
                employee.salary = salary
            await self.db.commit()
            await self.db.refresh(employee)
        return employee

    async def delete(self, employee_id: int):
        employee = await self.get(employee_id)
        if employee:
            await self.db.delete(employee)
            await self.db.commit()
        return employee
    
class ProccessDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, proccess_id: int):
        result = await self.db.execute(select(Proccess).where(Proccess.id == proccess_id))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(Proccess))
        return result.scalars().all()

    async def create(self, name: str):
        new_proccess = Proccess(name=name)
        self.db.add(new_proccess)
        await self.db.commit()
        await self.db.refresh(new_proccess)
        return new_proccess

    async def update(self, proccess_id: int, name: str):
        proccess = await self.get(proccess_id)
        if proccess:
            proccess.name = name
            await self.db.commit()
            await self.db.refresh(proccess)
        return proccess

    async def delete(self, proccess_id: int):
        proccess = await self.get(proccess_id)
        if proccess:
            await self.db.delete(proccess)
            await self.db.commit()
        return proccess
    
class ProccessEmployeeDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, process_employee_id: int):
        result = await self.db.execute(select(ProccessEmployee).where(ProccessEmployee.id == process_employee_id).options(joinedload(ProccessEmployee.employee)))
        return result.scalars().first()

    async def get_by_process_id(self, proccess_id: int):
        result = await self.db.execute(
            select(ProccessEmployee)
            .where(ProccessEmployee.proccess_id == proccess_id)
            .options(joinedload(ProccessEmployee.employee))
        )
        return result.scalars().all()

    async def create(self, proccess_id: int, employee_ids: List[int]):
        new_process_employees = []
        for employee_id in employee_ids:
            new_process_employee = ProccessEmployee(proccess_id=proccess_id, employee_id=employee_id)
            self.db.add(new_process_employee)
            new_process_employees.append(new_process_employee)
        await self.db.commit()
        for new_process_employee in new_process_employees:
            await self.db.refresh(new_process_employee)
        return new_process_employees

    async def update_by_process_id(self, proccess_id: int, employee_ids: List[int]):
        await self.delete_by_process_id(proccess_id)
        return await self.create(proccess_id, employee_ids)

    async def delete_by_process_id(self, proccess_id: int):
        process_employees = await self.get_by_process_id(proccess_id)
        for process_employee in process_employees:
            await self.db.delete(process_employee)
        await self.db.commit()

    async def delete_by_process_and_employee_id(self, proccess_id: int, employee_id: int):
        result = await self.db.execute(
            select(ProccessEmployee)
            .where(ProccessEmployee.proccess_id == proccess_id, ProccessEmployee.employee_id == employee_id)
        )
        process_employee = result.scalars().one_or_none()

        if process_employee:
            await self.db.delete(process_employee)
            await self.db.commit()
        return process_employee
    
class CompanyUserDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, company_user_id: int):
        result = await self.db.execute(select(CompanyUser).where(CompanyUser.id == company_user_id))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(CompanyUser))
        return result.scalars().all()

    async def create(self, company_id: int, user_id: int):
        new_company_user = CompanyUser(company_id=company_id, user_id=user_id)
        self.db.add(new_company_user)
        await self.db.commit()
        await self.db.refresh(new_company_user)
        return new_company_user

    async def update(self, company_user_id: int, company_id: Optional[int], user_id: Optional[int]):
        company_user = await self.get(company_user_id)
        if company_user:
            if company_id is not None:
                company_user.company_id = company_id
            if user_id is not None:
                company_user.user_id = user_id
            await self.db.commit()
            await self.db.refresh(company_user)
        return company_user

    async def delete(self, company_user_id: int):
        company_user = await self.get(company_user_id)
        if company_user:
            await self.db.delete(company_user)
            await self.db.commit()
        return company_user