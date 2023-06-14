from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    created_at: datetime
    class Config:
        orm_mode = True
class UserBase(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserCreate(UserBase):
    id:int
    is_active:bool
    is_superuser:bool
    created_at:datetime
class User(BaseModel):
    username:str
    email:str
    is_active:bool
    is_superuser:bool
    created_at:datetime
    class Config:
        orm_mode=True
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]






