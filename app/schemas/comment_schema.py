from pydantic import BaseModel
from typing import Optional

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class CommentUpdate(CommentBase):
    content: Optional[str] = None

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True
