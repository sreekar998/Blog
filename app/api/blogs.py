"""
Blog API endpoints for Blog application.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.blog import BlogCreate, BlogOut
from app.db.session import SessionLocal
from app.models.blog import Blog
from app.models.user import User
from app.api.users import get_current_user
from typing import List

router = APIRouter(prefix="/blogs", tags=["blogs"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[BlogOut])
def list_blogs(skip: int = 0, limit: int = Query(10, le=100), db: Session = Depends(get_db)):
    blogs = db.query(Blog).offset(skip).limit(limit).all()
    return blogs

@router.post("/", response_model=BlogOut)
def create_blog(blog_in: BlogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = Blog(title=blog_in.title, content=blog_in.content, author_id=current_user.id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

@router.get("/{id}", response_model=BlogOut)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{id}", response_model=BlogOut)
def update_blog(id: int, blog_in: BlogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    blog.title = blog_in.title
    blog.content = blog_in.content
    db.commit()
    db.refresh(blog)
    return blog

@router.delete("/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(blog)
    db.commit()
    return {"detail": "Blog deleted"}
