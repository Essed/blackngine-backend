from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .__init__ import UserCreate, UserBase, UserUpdate
from app.src.hasher import Hasher
from dependency import get_current_user_from_token

from app.db.dals import UserDAL
from app.db.session import get_db

user_router = APIRouter()

@user_router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)    
    existed_user = user_dal.get_by_email(user.email)
    if existed_user: 
        raise HTTPException(status_code=400, detail="User email already registered")
    user = user.model_dump()
    user['password'] = Hasher.get_password_hash(user['password'])    
    new_user = await user_dal.create(**user)
    return new_user

@user_router.get("/{user_id}")
async def read_user(user_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    db_user = await user_dal.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserBase(id = db_user.id, email = db_user.email, password = db_user.password)

@user_router.get("/")
async def read_users(current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    users = await user_dal.get_all()
    return users

@user_router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    updated_user = await user_dal.update(user_id, email=user.email, password=user.password)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@user_router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    user_dal = UserDAL(db)
    deleted_user = await user_dal.delete(user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}