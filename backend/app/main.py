"""Main FastAPI application initialization and configuration"""

import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import settings
from .database import engine
from .middleware.logging import user_journey_logger
from .middleware.security import add_security_headers
from .routers import (auth, cache, companies, contact, dashboard, public,
                      publishers, reports, skills)

# Configure module logger
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Validate JWT secret key on startup
try:
    settings.validate_jwt_secret()
except ValueError as e:
    logger.error(f"❌ Security Error: {e}")
    logger.error(
        "Please set a strong JWT_SECRET_KEY (at least 32 characters) in your environment variables."
    )
    exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="HireMetrics Jobs API",
    version="1.0.0",
    description="Job Market Analytics API for HireMetrics SaaS Platform",
)

# Add middleware
app.middleware("http")(add_security_headers)
app.middleware("http")(user_journey_logger)

# CORS middleware - Secure configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Content-Length", "Content-Range"],
    max_age=86400,  # Cache preflight requests for 24 hours
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(companies.router, prefix="/api/dashboard", tags=["Companies"])
app.include_router(publishers.router, prefix="/api/dashboard", tags=["Publishers"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(public.router, prefix="/api/public", tags=["Public"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(cache.router, prefix="/api/cache", tags=["Cache"])
app.include_router(contact.router, prefix="/api", tags=["Contact"])


# Root endpoints
@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "HireMetrics Jobs API",
        "version": "1.0.0",
        "description": "Job Market Analytics API for HireMetrics SaaS Platform",
        "endpoints": {
            "auth": "/api/auth",
            "dashboard": "/api/dashboard",
            "reports": "/api/reports",
            "user": "/api/user",
            "health": "/health",
            "docs": "/docs",
        },
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "HireMetrics Jobs API",
    }
