"""
Comment API endpoints for Blog application.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentOut
from app.db.session import SessionLocal
from app.models.comment import Comment
from app.models.blog import Blog
from app.models.user import User
from app.api.users import get_current_user
from typing import List

router = APIRouter(prefix="/comments", tags=["comments"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/blogs/{blog_id}/comments", response_model=CommentOut)
def add_comment(blog_id: int, comment_in: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    comment = Comment(text=comment_in.text, blog_id=blog_id, user_id=current_user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get("/blogs/{blog_id}/comments", response_model=List[CommentOut])
def get_comments(blog_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.blog_id == blog_id).all()
    return comments

@router.delete("/{id}")
def delete_comment(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    blog = db.query(Blog).filter(Blog.id == comment.blog_id).first()
    if comment.user_id != current_user.id and blog.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}
