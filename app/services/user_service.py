# app/service/user_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserLogin
import bcrypt
from app.models.user_model import User 
from datetime import timedelta
from app.core.security import create_access_token, get_current_user, check_user_permission
from app.config import settings

def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_admin(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_admin = User(username=user.username, email=user.email, password=hashed_password, isAdmin=True)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def login(db: Session, user_login: UserLogin):
    user = db.query(User).filter(User.email == user_login.email).first()
    
    if user is None:
        return {"message": "User không tồn tại"}
    
    if not bcrypt.checkpw(user_login.password.encode('utf-8'), user.password):
        return {"message": "Mật khẩu không chính xác"} 
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id},  
        expires_delta=access_token_expires,
        is_admin=user.isAdmin
    )
    
    user_response = UserResponse(id=user.id, username=user.username, email=user.email, isAdmin=user.isAdmin)
    
    return {
        "message": "Đăng nhập thành công",
        "user": user_response,
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_user(db: Session, user_id: int, authorization: str):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    requested_user = db.query(User).filter(User.id == user_id).first()
    if not requested_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return requested_user

def update_user(db: Session, user_id: int, user: UserUpdate, authorization: str ):
    current_user, is_admin = get_current_user(authorization, db)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Kiểm tra nếu user_id khác với ID của current_user và không phải admin
    if current_user.id != user_id and not is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to edit this user")

    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if existing_user:
        if user.username is not None:
            existing_user.username = user.username
        if user.email is not None:
            existing_user.email = user.email
        if user.password is not None:
            hashed_password = bcrypt.hashpw(user.password, bcrypt.gensalt())
            existing_user.password = hashed_password 
        
        db.commit()
        db.refresh(existing_user)
        return existing_user

    return None

def delete_user(db: Session, user_id: int, authorization: str ):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    check_user_permission(is_admin)
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user:
        db.delete(existing_user)
        db.commit()
        return True
    return False
