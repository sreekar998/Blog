"""
Tenant simulation middleware for FastAPI.
Requires X-Tenant-ID header if enabled.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import status
from starlette.responses import JSONResponse
from app.core.config import settings

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if settings.TENANT_REQUIRED:
            tenant_id = request.headers.get("X-Tenant-ID")
            if not tenant_id:
                return JSONResponse({"detail": "X-Tenant-ID header required"}, status_code=status.HTTP_400_BAD_REQUEST)
        response = await call_next(request)
        return response
