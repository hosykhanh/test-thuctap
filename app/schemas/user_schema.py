from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(..., example="username") 
    email: EmailStr = Field(..., example="email@example.com")
    isAdmin: bool = Field(default=False, example=False) 

class UserCreate(UserBase):
    password: str = Field(..., example="password123") 

class UserUpdate(UserBase):
    username: str | None = Field(None, example="newusername")
    email: EmailStr | None = Field(None, example="newemail@example.com")
    password: str | None = Field(None, example="newpassword123")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="email@example.com")
    password: str = Field(..., example="password123")

class UserResponse(UserBase):
    id: int = Field(..., example=1) 

    class Config:
        from_attributes = True
