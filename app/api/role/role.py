# api/role_api.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.config.database.database import get_db
from app.api.login.login import get_current_user
from app.services.role import role_service

router = APIRouter(
    prefix="/role",
    tags=['role']
)

@router.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return role_service.create_role(role, db)

@router.get("/roles/", response_model=List[schemas.Role])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return role_service.get_roles(skip, limit, db)

@router.get("/roles/{role_id}", response_model=schemas.Role)
def read_role(role_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return role_service.get_role_by_id(role_id, db)
