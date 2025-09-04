"""
Custom header middleware for FastAPI.
Adds X-App-Version to all responses.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-App-Version"] = "1.0.0"
        return response
