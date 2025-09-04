"""
Comment model for Blog application.
Uses SQLAlchemy ORM.
"""
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    blog = relationship("Blog", back_populates="comments")
    user = relationship("User", back_populates="comments")
