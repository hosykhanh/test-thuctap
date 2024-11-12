# app/service/post_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.post_schema import PostCreate, PostUpdate
from app.models.post_model import Post
from app.core.security import get_current_user

def create_post(db: Session, post: PostCreate, authorization: str):
    user, _ = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    new_post = Post(description=post.description, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post(db: Session, post_id: int, authorization: str):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

def get_all_posts(db: Session):
    posts = db.query(Post).all()
    return posts

def get_posts_by_user_id(db: Session, user_id: int, authorization: str):
    user, _ = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    return posts

def update_post(db: Session, post_id: int, post: PostUpdate, authorization: str):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    existing_post = db.query(Post).filter(Post.id == post_id).first()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if existing_post.user_id != user.id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    if post.description is not None:
        existing_post.description = post.description
    
    db.commit()
    db.refresh(existing_post)
    return existing_post

def delete_post(db: Session, post_id: int, authorization: str):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    existing_post = db.query(Post).filter(Post.id == post_id).first()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if existing_post.user_id != user.id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(existing_post)
    db.commit()
    return True
