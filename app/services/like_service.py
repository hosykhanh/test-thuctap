# app/services/like_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.like_model import Like
from app.core.security import get_current_user
from app.schemas.like_schema import LikeCreate

def add_like(db: Session, like_data: LikeCreate, authorization: str) -> Like:
    user, _ = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    existing_like = db.query(Like).filter(Like.post_id == like_data.post_id, Like.user_id == user.id).first()
    if existing_like:
        existing_like.is_like = like_data.is_like  # Update like status
    else:
        new_like = Like(post_id=like_data.post_id, user_id=user.id, is_like=like_data.is_like)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like
    
    db.commit()
    db.refresh(existing_like)
    return existing_like

def get_like(db: Session, like_id: int, authorization: str):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    like = db.query(Like).filter(Like.id == like_id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    return like

def get_likes_by_post_id(db: Session, post_id: int):
    return db.query(Like).filter(Like.post_id == post_id).all()

def remove_like(db: Session, post_id: int, authorization: str):
    user, _ = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user.id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()
    return True
