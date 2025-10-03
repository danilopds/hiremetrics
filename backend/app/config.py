import os
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 50

    # Frontend URLs for redirects
    FRONTEND_URL: str = "http://localhost:5173"

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None

    # CORS Configuration
    CORS_ORIGINS: Optional[str] = None  # Comma-separated string from environment

    # Default development origins
    DEFAULT_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Environment-based CORS configuration
    @property
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins based on environment"""
        # Allow environment variable override
        if self.CORS_ORIGINS:
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

        # Development origins
        if os.getenv("ENVIRONMENT", "development") == "development":
            return self.DEFAULT_CORS_ORIGINS

        # Production origins - should be set via environment variable
        return []

    def validate_jwt_secret(self) -> None:
        """Validate JWT secret key strength"""
        if len(self.JWT_SECRET_KEY) < 32:
            raise ValueError(
                "JWT_SECRET_KEY must be at least 32 characters long for security. "
                "Current length: {} characters".format(len(self.JWT_SECRET_KEY))
            )

    # class Config:
    #    env_file = ".env"


settings = Settings()
