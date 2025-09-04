"""
App configuration settings.
"""
import os

class Settings:
    PROJECT_NAME: str = "Blog API"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    APP_VERSION: str = "1.0.0"
    TENANT_REQUIRED: bool = False

settings = Settings()
