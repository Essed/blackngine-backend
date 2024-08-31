from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .__init__ import CompanyCreate, CompanyUpdate, CompanyBase, UserBase
from dependency import get_current_user_from_token

from app.db.dals import CompanyDAL
from app.db.session import get_db

company_router = APIRouter()

@company_router.post("/", response_model=CompanyBase)
async def create_company(company: CompanyCreate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    company_dal = CompanyDAL(db)
    created_company = company.model_dump()
    company = await company_dal.get_by_name(**created_company) 
    if company is not None:
        raise HTTPException(status_code=400, detail="Company name already registered")
    new_company = await company_dal.create(**created_company)
    return new_company

@company_router.get("/{company_id}", response_model=CompanyBase)
async def read_company(company_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    company_dal = CompanyDAL(db)
    company = await company_dal.get(company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@company_router.get("/", response_model=list[CompanyBase])
async def read_companies(current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    company_dal = CompanyDAL(db)
    companies = await company_dal.get_all()
    return companies

@company_router.put("/{company_id}", response_model=CompanyBase)
async def update_company(company_id: int, company: CompanyUpdate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    company_dal = CompanyDAL(db)
    updated_company = await company_dal.update(company_id, name=company.name)
    if updated_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated_company

@company_router.delete("/{company_id}")
async def delete_company(company_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    company_dal = CompanyDAL(db)
    deleted_company = await company_dal.delete(company_id)
    if deleted_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"detail": "Company deleted successfully"}