from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .__init__ import  CompanyUserBase, CompanyUserCreate, CompanyUserUpdate, UserBase
from dependency import get_current_user_from_token
from typing import List

from app.db.dals import CompanyUserDAL
from app.db.session import get_db

company_user_router = APIRouter()

@company_user_router.post("/", response_model=CompanyUserBase)
async def create_company_user(company_user: CompanyUserCreate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = CompanyUserDAL(db)
    new_company_user = await dal.create(company_id=company_user.company_id, user_id=company_user.user_id)
    return new_company_user

@company_user_router.get("/{company_user_id}", response_model=CompanyUserBase)
async def read_company_user(company_user_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = CompanyUserDAL(db)
    db_company_user = await dal.get(company_user_id)
    if db_company_user is None:
        raise HTTPException(status_code=404, detail="CompanyUser not found")
    return db_company_user

@company_user_router.get("/", response_model=list[CompanyUserBase])
async def read_company_users(current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = CompanyUserDAL(db)
    company_users = await dal.get_all()
    return company_users

@company_user_router.put("/{company_user_id}", response_model=CompanyUserBase)
async def update_company_user(company_user_id: int, company_user: CompanyUserUpdate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = CompanyUserDAL(db)
    updated_company_user = await dal.update(company_user_id, company_user.company_id, company_user.user_id)
    if updated_company_user is None:
        raise HTTPException(status_code=404, detail="CompanyUser not found")
    return updated_company_user

@company_user_router.delete("/{company_user_id}")
async def delete_company_user(company_user_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    dal = CompanyUserDAL(db)
    deleted_company_user = await dal.delete(company_user_id)
    if deleted_company_user is None:
        raise HTTPException(status_code=404, detail="CompanyUser not found")
    return {"detail": "CompanyUser deleted successfully"}