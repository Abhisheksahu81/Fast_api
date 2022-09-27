from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class CreatePost(PostBase):
    pass

#response model after creating user
class Userout(BaseModel):
    id : int 
    email : EmailStr
    created_at : datetime
    class Config: 
      orm_mode = True

class Post(BaseModel):
    id : int
    title : str
    content : str
    published : bool = True
    created_at : datetime
    owner_id : int
    owner : Userout

    class Config : 
     orm_mode = True

class PostOut(BaseModel):
    Post : Post
    votes : int
    
    class Config : 
     orm_mode = True      

class UserCreate(BaseModel):
    email : EmailStr
    password : str     



class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenData(BaseModel):
    id : Optional[str] = None

class Token(BaseModel):
    access_token : str
    token_type : str

class Vote(BaseModel):
    post_id : int
    dir : conint(le = 1)