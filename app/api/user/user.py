# api/user_api.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas as schemas
from app.api.login.login import get_current_user
from app.config.database.database import get_db
from app.services.user import user_service

router = APIRouter(
    prefix="/user",
    tags=['user']
)

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user_service.create_user(user, db)

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user_service.get_users(skip, limit, db)

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user_service.get_user_by_id(user_id, db)

@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user_service.update_user(user_id, user, db)
