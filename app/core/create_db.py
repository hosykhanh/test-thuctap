from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = "sqlite:///./test_database.db"  

def create_database():
    # Tạo engine và session
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Tạo tất cả các bảng
    Base.metadata.create_all(bind=engine)

    print("Database and tables created successfully.")

