from sqlalchemy import Column, Integer, String, ForeignKey
from .user_model import Base

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
