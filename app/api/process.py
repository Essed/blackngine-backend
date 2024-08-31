from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .__init__ import  ProcessBase, ProcessCreate, ProcessUpdate, UserBase
from dependency import get_current_user_from_token

from app.db.dals import ProccessDAL
from app.db.session import get_db


proccess_router = APIRouter()

@proccess_router.post("/", response_model=ProcessBase)
async def create_process(process: ProcessCreate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    process_dal = ProccessDAL(db)
    new_process = await process_dal.create(name=process.name)
    return new_process

@proccess_router.get("/{process_id}", response_model=ProcessBase)
async def read_process(process_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    process_dal = ProccessDAL(db)
    db_process = await process_dal.get(process_id)
    if db_process is None:
        raise HTTPException(status_code=404, detail="Process not found")
    return db_process

@proccess_router.get("/", response_model=list[ProcessBase])
async def read_processes(current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    process_dal = ProccessDAL(db)
    processes = await process_dal.get_all()
    return processes

@proccess_router.put("/{process_id}", response_model=ProcessBase)
async def update_process(process_id: int, process: ProcessUpdate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    process_dal = ProccessDAL(db)
    updated_process = await process_dal.update(process_id, name=process.name)
    if updated_process is None:
        raise HTTPException(status_code=404, detail="Process not found")
    return updated_process

@proccess_router.delete("/{process_id}")
async def delete_process(process_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    process_dal = ProccessDAL(db)
    deleted_process = await process_dal.delete(process_id)
    if deleted_process is None:
        raise HTTPException(status_code=404, detail="Process not found")
    return {"detail": "Process deleted successfully"}