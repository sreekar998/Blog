"""
Request logging middleware for FastAPI.
Logs method, path, and response time.
"""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        print(f"{request.method} {request.url.path} completed in {process_time:.2f}ms")
        return response
