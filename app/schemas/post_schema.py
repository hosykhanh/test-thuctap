from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    description: str

class PostCreate(PostBase):
    user_id: int

class PostUpdate(PostBase):
    description: Optional[str] = None

class PostResponse(PostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
