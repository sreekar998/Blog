"""
Pydantic schemas for Comment model.
"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserOut

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    user: UserOut
    created_at: datetime

    class Config:
        orm_mode = True
