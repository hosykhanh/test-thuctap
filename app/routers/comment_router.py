# app/routers/comment_router.py
from fastapi import APIRouter, HTTPException, Depends, Security
from sqlalchemy.orm import Session
from app.core.config import get_db_connection
from app.schemas.comment_schema import CommentCreate, CommentUpdate, CommentResponse
from app.services.comment_service import create_comment, get_comment, update_comment, delete_comment, get_all_comments, get_comments_by_post_id
from fastapi.security import HTTPBearer
from typing import List

router = APIRouter()

security_scheme = HTTPBearer()

@router.post("/", response_model=CommentResponse)
def api_create_comment(comment: CommentCreate, authorization: str = Security(security_scheme), db: Session = Depends(get_db_connection)):
    new_comment = create_comment(db, comment, authorization)
    return CommentResponse(id=new_comment.id, content=new_comment.content, post_id=new_comment.post_id, user_id=new_comment.user_id)

@router.get("/{comment_id}", response_model=CommentResponse)
def api_get_comment(comment_id: int, db: Session = Depends(get_db_connection), authorization: str = Security(security_scheme)):
    comment = get_comment(db, comment_id, authorization)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return CommentResponse(id=comment.id, content=comment.content, post_id=comment.post_id, user_id=comment.user_id)

@router.get("/", response_model=List[CommentResponse])
def api_get_all_comments(db: Session = Depends(get_db_connection)):
    comments = get_all_comments(db)
    return [CommentResponse(id=comment.id, content=comment.content, post_id=comment.post_id, user_id=comment.user_id) for comment in comments]

@router.get("/post/{post_id}", response_model=List[CommentResponse])
def api_get_comments_by_post_id(post_id: int, db: Session = Depends(get_db_connection), authorization: str = Security(security_scheme)):
    comments = get_comments_by_post_id(db, post_id, authorization)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this post")
    return [CommentResponse(id=comment.id, content=comment.content, post_id=comment.post_id, user_id=comment.user_id) for comment in comments]

@router.put("/{comment_id}")
def api_update_comment(comment_id: int, comment: CommentUpdate, authorization: str = Security(security_scheme), db: Session = Depends(get_db_connection)):
    updated_comment = update_comment(db, comment_id, comment, authorization)
    if updated_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment updated successfully"}

@router.delete("/{comment_id}")
def api_delete_comment(comment_id: int, authorization: str = Security(security_scheme), db: Session = Depends(get_db_connection)):
    if not delete_comment(db, comment_id, authorization):
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
