from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models.models import User,Role,Permission
from fastapi import HTTPException, status

import os 


from dotenv import load_dotenv, dotenv_values 


load_dotenv(dotenv_path="../app/")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:

    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def add_user_with_role_and_permission(db: Session, username: str, email: str, password: str, role_name: str, permission_name: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        hashed_password = pwd_context.hash(password)
        user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"User '{username}' created.")
    else:
        print(f"User '{username}' already exists.")
    
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        role = Role(name=role_name)
        db.add(role)
        db.commit()
        db.refresh(role)
        print(f"Role '{role_name}' created.")
    else:
        print(f"Role '{role_name}' already exists.")
    
    permission = db.query(Permission).filter(Permission.name == permission_name).first()
    if not permission:
        permission = Permission(name=permission_name)
        db.add(permission)
        db.commit()
        db.refresh(permission)
        print(f"Permission '{permission_name}' created.")
    else:
        print(f"Permission '{permission_name}' already exists.")
    
    if role not in user.roles:
        user.roles.append(role)
        print(f"Role '{role_name}' added to user '{username}'.")
    
    if permission not in role.permissions:
        role.permissions.append(permission)
        print(f"Permission '{permission_name}' added to role '{role_name}'.")
    
    db.commit()
    db.refresh(user)
    db.refresh(role)
    
    print(f"User '{username}' updated with role '{role_name}' and permission '{permission_name}'")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
