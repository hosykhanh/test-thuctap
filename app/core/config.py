from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

DATABASE_URL = "sqlite:///./test_database.db"  

# Tạo engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Tạo sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Hàm để lấy session
def get_db_connection() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db  
    finally:
        db.close() 
