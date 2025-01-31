from sqlalchemy.orm import Session
from app.models import models as models
from app.schemas import schemas as schemas

def create_permission_service(permission: schemas.PermissionCreate, db: Session):
    db_permission = models.Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def read_permissions_service(skip: int, limit: int, db: Session):
    return db.query(models.Permission).offset(skip).limit(limit).all()

def read_permission_service(permission_id: int, db: Session):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()
