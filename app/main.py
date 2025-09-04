"""
Main FastAPI application entrypoint.
"""
from fastapi import FastAPI
from app.middleware.logging import LoggingMiddleware
from app.middleware.headers import CustomHeaderMiddleware
from app.middleware.tenant import TenantMiddleware
from app.api.users import router as users_router
from app.api.blogs import router as blogs_router
from app.api.comments import router as comments_router
from app.core.config import settings

app = FastAPI(title="Blog API", version=settings.APP_VERSION)

# Add custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(CustomHeaderMiddleware)
if settings.TENANT_REQUIRED:
    app.add_middleware(TenantMiddleware)

# Include routers
app.include_router(users_router)
app.include_router(blogs_router)
app.include_router(comments_router)
