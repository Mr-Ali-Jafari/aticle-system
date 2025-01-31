from sqlalchemy.orm import Session
from app.models import models as models
from app.schemas import schemas as schemas
from fastapi import HTTPException, status
import logging

def create_user(user: schemas.UserCreate, db: Session):
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    for role_id in user.role_ids:
        role = db.query(models.Role).filter(models.Role.id == role_id).first()
        if role:
            db_user.roles.append(role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(skip: int, limit: int, db: Session):
    try:
        users = db.query(models.User).offset(skip).limit(limit).all()
        return users
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

def get_user_by_id(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(user_id: int, user: schemas.UserCreate, db: Session):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.hashed_password = user.password  

    db_user.roles = []  
    for role_id in user.role_ids:
        role = db.query(models.Role).filter(models.Role.id == role_id).first()
        if role:
            db_user.roles.append(role)

    db.commit()
    db.refresh(db_user)
    return db_user
