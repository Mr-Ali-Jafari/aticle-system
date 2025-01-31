from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.utils.auth_jwt import *
from app.schemas import schemas as schemas
from app.config.database.database import get_db
from app.api.login.login import get_current_user
from app.services.permission.permission_service import (
    create_permission_service,
    read_permissions_service,
    read_permission_service,
)

router = APIRouter(
    prefix="/permission",
    tags=['permission']
)

@router.post("/permissions/", response_model=schemas.Permission)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):

    return create_permission_service(permission, db)

@router.get("/permissions/", response_model=List[schemas.Permission])
def read_permissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return read_permissions_service(skip, limit, db)

@router.get("/permissions/{permission_id}", response_model=schemas.Permission)
def read_permission(permission_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    permission = read_permission_service(permission_id, db)
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission
