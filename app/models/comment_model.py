from sqlalchemy import Column, Integer, String, ForeignKey
from .user_model import Base

class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
