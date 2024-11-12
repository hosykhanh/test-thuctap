# app/routers/post_router.py
from fastapi import APIRouter, HTTPException, Depends, Security
from sqlalchemy.orm import Session
from app.core.config import get_db_connection
from app.schemas.post_schema import PostCreate, PostUpdate, PostResponse
from app.services.post_service import create_post, get_post, update_post, delete_post, get_all_posts, get_posts_by_user_id
from fastapi.security import HTTPBearer
from typing import List

router = APIRouter()

security_scheme = HTTPBearer()

@router.post("/", response_model=PostResponse)
def api_create_post(post: PostCreate, authorization: str = Security(security_scheme), db: Session = Depends(get_db_connection)):
    new_post = create_post(db, post, authorization)
    return PostResponse(id=new_post.id, description=new_post.description, user_id=new_post.user_id)

@router.get("/{post_id}", response_model=PostResponse)
def api_get_post(post_id: int, db: Session = Depends(get_db_connection), authorization: str = Security(security_scheme)):
    post = get_post(db, post_id, authorization)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponse(id=post.id, description=post.description, user_id=post.user_id)

@router.get("/", response_model=PostResponse)
def api_get_all_posts(db: Session = Depends(get_db_connection)):
    posts = get_all_posts(db)
    return [PostResponse(id=post.id, description=post.description, user_id=post.user_id) for post in posts]

@router.get("/user/{user_id}", response_model=List[PostResponse])
def api_get_posts_by_user_id(user_id: int, db: Session = Depends(get_db_connection), authorization: str = Security(security_scheme)):
    posts = get_posts_by_user_id(db, user_id, authorization)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")
    return [PostResponse(id=post.id, description=post.description, user_id=post.user_id) for post in posts]

@router.put("/{post_id}")
def api_update_post(post_id: int, post: PostUpdate, authorization: str = Security(security_scheme), db: Session = Depends(get_db_connection)):
    updated_post = update_post(db, post_id, post, authorization)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post updated successfully"}

@router.delete("/{post_id}")
def api_delete_post(post_id: int, authorization: str = Security(security_scheme), db: Session = Depends(get_db_connection)):
    if not delete_post(db, post_id, authorization):
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
