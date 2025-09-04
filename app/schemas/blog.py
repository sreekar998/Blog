"""
Pydantic schemas for Blog model.
"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.user import UserOut

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int
    author: UserOut
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
