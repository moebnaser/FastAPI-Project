from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate (PostBase):
    pass

class UserOut (BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase): # response schema (pydantic modekl)
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        orm_mode = True  #converts the response from SQL alchemy modele to pydantic model for the response 

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin (BaseModel):
    email: EmailStr
    password: str

class Token (BaseModel):
    access_token: str
    token_type: str

class TokenData (BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]

class PostOut (BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True