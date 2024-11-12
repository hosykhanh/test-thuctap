from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY", "your_default_secret_key")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    
    app_name: str = "APP TEST THUC TAP"
    debug: bool = True

    class Config:
        env_file = ".env" 

settings = Settings()
