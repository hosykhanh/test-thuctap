# app/routers/like_router.py
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.core.config import get_db_connection
from app.services.like_service import add_like, get_likes_by_post_id, remove_like, get_like
from app.schemas.like_schema import LikeCreate, LikeResponse
from fastapi.security import HTTPBearer
from typing import List

router = APIRouter()

security_scheme = HTTPBearer()

@router.post("/post/{post_id}/like", response_model=LikeResponse)
def api_add_like(like_data: LikeCreate, db: Session = Depends(get_db_connection), authorization: str = Security(security_scheme)):
    new_like = add_like(db, like_data, authorization)
    return LikeResponse.model_validate(new_like)

@router.get("/{like_id}", response_model=LikeResponse)
def api_get_like(like_id: int, db: Session = Depends(get_db_connection), authorization: str = Security(security_scheme)):
    like = get_like(db, like_id, authorization)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    return LikeResponse.model_validate(like)

@router.get("/post/{post_id}/likes", response_model=List[LikeResponse])
def api_get_likes_by_post_id(post_id: int, db: Session = Depends(get_db_connection)):
    likes = get_likes_by_post_id(db, post_id)
    if not likes:
        raise HTTPException(status_code=404, detail="No likes found for this post")
    return [LikeResponse.model_validate(like) for like in likes]

@router.delete("/post/{post_id}/like")
def api_remove_like(post_id: int, db: Session = Depends(get_db_connection), authorization: str = Security(security_scheme)):
    if not remove_like(db, post_id, authorization):
        raise HTTPException(status_code=404, detail="Like not found")
    return {"message": "Like removed successfully"}
