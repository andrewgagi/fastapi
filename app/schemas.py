from datetime import datetime
from pydantic import BaseModel

    
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
    email:str
    password:str

class UserCreate(UserBase):
    id:int
    is_active:bool
    is_superuser:bool
    created_at:datetime
class User(UserBase):
    is_active:bool
    is_superuser:bool
    created_at:datetime
    class Config:
        orm_mode=True



