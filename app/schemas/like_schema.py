from pydantic import BaseModel

class LikeBase(BaseModel):
    is_like: bool

class LikeCreate(LikeBase):
    post_id: int

class LikeResponse(LikeBase):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True
