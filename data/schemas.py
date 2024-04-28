from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str


class TopicCreate(BaseModel):
    name: str
    category_id: int
    best_reply_id: Optional[int] = None


class Topic(BaseModel):
    topic_name: str
    category_id: int
    created_at: Optional[datetime] = None
    best_reply_id: Optional[int] = None


class CreateCategory(BaseModel):
    name: str
    is_private: Optional[bool] = None
    is_locked: Optional[bool] = None


class CategoryOut(CreateCategory):
    name: str
    id: int
    created_at: str
