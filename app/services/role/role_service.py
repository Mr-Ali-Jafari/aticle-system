from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from fastapi import HTTPException, status

def create_role(role: schemas.RoleCreate, db: Session):
    db_role = models.Role(name=role.name)
    for permission_id in role.permission_ids:
        permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
        if permission:
            db_role.permissions.append(permission)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(skip: int, limit: int, db: Session):
    roles = db.query(models.Role).offset(skip).limit(limit).all()
    return roles

def get_role_by_id(role_id: int, db: Session):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
