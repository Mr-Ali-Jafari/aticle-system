from sqlalchemy.orm import Session
from app.models import models as models
from app.utils.auth_jwt.auth import *
from fastapi import HTTPException, status
from datetime import timedelta
import logging

ACCESS_TOKEN_EXPIRE_MINUTES = 30 

def authenticate_user_service(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def login_for_access_token_service(db: Session, form_data):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if user:
        failed_attempt = db.query(models.FailedLoginAttempt).filter(models.FailedLoginAttempt.user_id == user.id).first()

        if failed_attempt and failed_attempt.block_until:
            current_time = datetime.utcnow()
            if current_time < failed_attempt.block_until:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You are blocked until {failed_attempt.block_until}.",
                )

    authenticated_user = authenticate_user_service(db, form_data.username, form_data.password)

    if not authenticated_user:
        if user:
            if failed_attempt:
                failed_attempt.attempts += 1
            else:
                failed_attempt = models.FailedLoginAttempt(user_id=user.id, attempts=1)
                db.add(failed_attempt)

            # بلاک کردن کاربر بر اساس تعداد تلاش‌ها
            if failed_attempt.attempts >= 3 and failed_attempt.attempts < 6:
                failed_attempt.block_until = datetime.utcnow() + timedelta(minutes=5)
            elif failed_attempt.attempts >= 6:
                failed_attempt.block_until = datetime.utcnow() + timedelta(minutes=10)

            db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if failed_attempt:
        failed_attempt.attempts = 0
        failed_attempt.block_until = None
        db.commit()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user_service(db: Session, token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(models.User).filter(models.User.username == payload.get("sub")).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
