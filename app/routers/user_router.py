# app/routers/user_router.py
from fastapi import APIRouter, HTTPException, Depends, Security
from sqlalchemy.orm import Session
from app.core.config import get_db_connection
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserLogin
from app.services.user_service import create_user, create_admin, get_user, update_user, delete_user, login
from fastapi.security import HTTPBearer

router = APIRouter()

security_scheme = HTTPBearer()

@router.post("/", response_model=UserResponse)
def api_create_user(user: UserCreate, db: Session = Depends(get_db_connection)):
    new_user = create_user(db, user)
    return UserResponse(id=new_user.id, username=new_user.username, email=new_user.email, isAdmin=new_user.isAdmin)

@router.post("/admins", response_model=UserResponse)
def api_create_admin(user: UserCreate, db: Session = Depends(get_db_connection)):
    new_admin = create_admin(db, user)
    return UserResponse(id=new_admin.id, username=new_admin.username, email=new_admin.email, isAdmin=new_admin.isAdmin)

@router.post("/login")
def api_login(user_login: UserLogin, db: Session = Depends(get_db_connection)):
    return login(db, user_login)

@router.get("/{user_id}", response_model=UserResponse)
def api_get_user(user_id: int, db: Session = Depends(get_db_connection), authorization: str = Security(security_scheme)):
    print(authorization)
    user = get_user(db, user_id, authorization)
    return UserResponse(id=user.id, username=user.username, email=user.email, isAdmin=user.isAdmin)

@router.put("/{user_id}")
def api_update_user(user_id: int, user: UserUpdate, authorization: str = Security(security_scheme), db: Session = Depends(get_db_connection)):
    updated_user = update_user(db, user_id, user, authorization)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@router.delete("/{user_id}")
def api_delete_user(user_id: int, authorization: str = Security(security_scheme), db: Session = Depends(get_db_connection)):
    if not delete_user(db, user_id, authorization):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
