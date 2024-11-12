from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.comment_model import Comment
from app.core.security import get_current_user
from app.schemas.comment_schema import CommentCreate, CommentUpdate

def create_comment(db: Session, comment: CommentCreate, authorization: str):
    user, _ = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    new_comment = Comment(content=comment.content, post_id=comment.post_id, user_id=user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comment(db: Session, comment_id: int, authorization: str):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

def get_all_comments(db: Session):
    comments = db.query(Comment).all()
    return comments

def get_comments_by_post_id(db: Session, post_id: int, authorization: str):
    user, _ = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

def update_comment(db: Session, comment_id: int, comment: CommentUpdate, authorization: str):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    existing_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if existing_comment.user_id != user.id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    
    if comment.content is not None:
        existing_comment.content = comment.content
    
    db.commit()
    db.refresh(existing_comment)
    return existing_comment

def delete_comment(db: Session, comment_id: int, authorization: str):
    user, is_admin = get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    existing_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if existing_comment.user_id != user.id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(existing_comment)
    db.commit()
    return True
