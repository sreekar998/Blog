
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import SessionLocal

# Create a separate test database (file-based for persistence across requests)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[SessionLocal] = TestingSessionLocal
for route in app.routes:
    if hasattr(route, "dependant"):
        for dep in route.dependant.dependencies:
            if hasattr(dep, "call") and dep.call.__name__ == "get_db":
                dep.call = override_get_db

client = TestClient(app)

def test_root_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_register_and_login():
    # Register
    user = {"username": "testuser", "email": "testuser@example.com", "password": "testpass"}
    response = client.post("/users/register", json=user)
    assert response.status_code in (200, 400)  # 400 if already exists
    # Login
    data = {"username": "testuser", "password": "testpass"}
    response = client.post("/users/login", data=data)
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    return tokens["access_token"]

def test_blog_crud():
    token = test_register_and_login()
    headers = {"Authorization": f"Bearer {token}"}
    # Create blog
    blog = {"title": "Test Blog", "content": "Test content."}
    response = client.post("/blogs/", json=blog, headers=headers)
    assert response.status_code == 200
    blog_id = response.json()["id"]
    # Get blog
    response = client.get(f"/blogs/{blog_id}")
    assert response.status_code == 200
    # Update blog
    update = {"title": "Updated Blog", "content": "Updated content."}
    response = client.put(f"/blogs/{blog_id}", json=update, headers=headers)
    assert response.status_code == 200
    # Delete blog
    response = client.delete(f"/blogs/{blog_id}", headers=headers)
    assert response.status_code == 200

def test_comment_crud():
    token = test_register_and_login()
    headers = {"Authorization": f"Bearer {token}"}
    # Create blog for comment
    blog = {"title": "Blog for Comment", "content": "Content."}
    response = client.post("/blogs/", json=blog, headers=headers)
    blog_id = response.json()["id"]
    # Add comment
    comment = {"text": "Nice post!"}
    response = client.post(f"/comments/blogs/{blog_id}/comments", json=comment, headers=headers)
    assert response.status_code == 200
    comment_id = response.json()["id"]
    # Get comments
    response = client.get(f"/comments/blogs/{blog_id}/comments")
    assert response.status_code == 200
    # Delete comment
    response = client.delete(f"/comments/{comment_id}", headers=headers)
    assert response.status_code == 200
