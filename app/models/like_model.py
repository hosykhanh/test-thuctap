from sqlalchemy import Column, Integer, Boolean, ForeignKey
from .user_model import Base

class Like(Base):
    __tablename__ = 'Like'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_like = Column(Boolean, nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
