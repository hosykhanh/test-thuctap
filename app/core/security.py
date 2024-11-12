# app/core/security.py
from fastapi import HTTPException, Depends, Header
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from app.models.user_model import User
from app.core.config import get_db_connection 
from sqlalchemy.orm import Session
from app.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security_scheme = HTTPBearer()

secret_key = settings.secret_key
access_token_expire_minutes = settings.access_token_expire_minutes
algorithm = settings.algorithm

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, is_admin: bool = False):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=access_token_expire_minutes))
    to_encode.update({"exp": expire, "sub": str(data.get("sub")), "isAdmin": is_admin})  # Thêm isAdmin vào payload
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def verify_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: str = payload.get("sub")
        is_admin: bool = payload.get("isAdmin")
        
        if user_id is None or is_admin is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = int(user_id)
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user, is_admin
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security_scheme), db: Session = Depends(get_db_connection)):
    # Lấy token từ credentials
    token = authorization.credentials if authorization else None
    if not token:
        raise HTTPException(status_code=401, detail="Token missing or malformed")
    
    # Giả sử hàm verify_token trả về user và quyền admin
    user, is_admin = verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user, is_admin

def check_user_permission(is_admin: bool):
    if not is_admin: 
        raise HTTPException(status_code=403, detail="Not enough permissions")
