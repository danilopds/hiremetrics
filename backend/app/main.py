from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Query,
    Request,
    Body,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, RedirectResponse
from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from .utils.auth_utils import create_access_token, get_current_user
from sqlalchemy import text
import os
import io
import csv
import requests
from collections import defaultdict
import json
import time
import base64

# Configure module logger
logger = logging.getLogger(__name__)

from .database import get_db, engine
from . import models, schemas, crud
from .config import settings
from .schemas import (
    JobDashboardBase,
    TopSkill,
    CSVExportFilters,
    CSVExportRequest,
    ExportCountResponse,
    ContactForm,
    ContactResponse,
)
from .utils.query_builder import SecureQueryBuilder
from .utils.cache import cache_result, query_cache

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Validate JWT secret key on startup
try:
    settings.validate_jwt_secret()
except ValueError as e:
    print(f"❌ Security Error: {e}")
    print(
        "Please set a strong JWT_SECRET_KEY (at least 32 characters) in your environment variables."
    )
    exit(1)

# Cache for storing client tokens by IP to consistently identify users
client_token_cache = defaultdict(lambda: {"token": None, "timestamp": 0})

app = FastAPI(title="Jobs API")


# Root endpoint
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


# Health check endpoint for deployment monitoring
@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "HireMetrics Jobs API",
    }


# Security middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)

    # Security headers
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    # HSTS header (only for HTTPS)
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )

    return response


# User journey logger middleware
@app.middleware("http")
async def user_journey_logger(request: Request, call_next):
    """Log user journey with properly identified user"""
    # Only log API requests
    if not request.url.path.startswith("/api/"):
        return await call_next(request)

    # Skip logging for certain endpoints (like health checks)
    if request.url.path == "/api/health":
        return await call_next(request)

    # Get client IP for token caching
    client_ip = request.client.host if request.client else "unknown"

    # Process the request
    response = await call_next(request)

    # Extract user ID from Authorization header
    user_id = "anonymous"
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix

        # Store token in cache by client IP for future requests
        client_token_cache[client_ip] = {"token": token, "timestamp": time.time()}

        try:
            # Extract payload from JWT without verification
            # Format is typically header.payload.signature
            parts = token.split(".")
            if len(parts) == 3:
                # Fix padding for base64 decoding
                payload = parts[1]
                payload += "=" * ((4 - len(payload) % 4) % 4)

                # Decode payload
                decoded_payload = base64.urlsafe_b64decode(payload)
                payload_data = json.loads(decoded_payload)

                # Extract user email as ID
                if "sub" in payload_data:
                    user_id = payload_data["sub"]
        except Exception as e:
            # Log the error for debugging but fall back to anonymous
            logger.debug(f"Failed to parse JWT token: {e}")
            pass
    else:
        # Try to get user ID from cached token (for consistent tracking across requests)
        cached_data = client_token_cache[client_ip]
        if (
            cached_data["token"] and time.time() - cached_data["timestamp"] < 3600
        ):  # 1 hour TTL
            token = cached_data["token"]
            try:
                # Extract payload from JWT without verification
                parts = token.split(".")
                if len(parts) == 3:
                    payload = parts[1]
                    payload += "=" * ((4 - len(payload) % 4) % 4)

                    decoded_payload = base64.urlsafe_b64decode(payload)
                    payload_data = json.loads(decoded_payload)

                    if "sub" in payload_data:
                        user_id = payload_data["sub"]
            except Exception as e:
                logger.debug(f"Failed to parse cached JWT token: {e}")
                pass

    # Log only the user ID
    print(f"USER: user_id={user_id}")

    return response


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

# Authentication is now handled in utils/auth_utils.py


def create_user_token(
    user: models.User, expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token for user"""

    data = {
        "sub": user.email,
        "auth_provider": getattr(user, "auth_provider", "email"),  # Handle OAuth users
    }
    return create_access_token(data, expires_delta)


async def send_verification_email(email: str, token: str):
    """Send email verification email"""
    try:
        from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
        import os

        # Email configuration
        conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),
            MAIL_FROM=os.getenv("MAIL_FROM", "your-email@gmail.com"),
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        # Create verification URL
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        verification_url = f"{frontend_url}/auth/verify-email?token={token}"

        # Create email message
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Bem-vindo ao HireMetrics!</h2>
            <p>Obrigado por se registrar. Para ativar sua conta e começar a usar a plataforma, clique no botão abaixo:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}" 
                   style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Verificar Email
                </a>
            </div>
            
            <p>Ou copie e cole este link no seu navegador:</p>
            <p style="word-break: break-all; color: #6b7280;">{verification_url}</p>
            
            <p><strong>Importante:</strong></p>
            <ul>
                <li>Este link expira em 24 horas</li>
                <li>Após a verificação, você terá acesso completo à plataforma</li>
                <li>Se você não solicitou este registro, pode ignorar este email</li>
            </ul>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
            <p style="color: #6b7280; font-size: 14px;">
                Este email foi enviado automaticamente. Não responda a este email.
            </p>
        </div>
        """

        message = MessageSchema(
            subject="Verifique seu email - HireMetrics",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        # Send email
        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        print(f"Error sending verification email: {e}")
        raise e


async def send_password_reset_email(email: str, token: str):
    """Send password reset email"""
    try:
        from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
        import os

        # Email configuration
        conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),
            MAIL_FROM=os.getenv("MAIL_FROM", "your-email@gmail.com"),
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        # Create reset URL
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        reset_url = f"{frontend_url}/auth/reset-password/{token}"

        # Create email message
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Redefinir Senha - HireMetrics</h2>
            <p>Você solicitou a redefinição da sua senha. Para criar uma nova senha, clique no botão abaixo:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Redefinir Senha
                </a>
            </div>
            
            <p>Ou copie e cole este link no seu navegador:</p>
            <p style="word-break: break-all; color: #6b7280;">{reset_url}</p>
            
            <p><strong>Importante:</strong></p>
            <ul>
                <li>Este link expira em 1 hora</li>
                <li>Se você não solicitou esta redefinição, pode ignorar este email</li>
                <li>Sua senha atual permanecerá inalterada se você não clicar no link</li>
            </ul>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
            <p style="color: #6b7280; font-size: 14px;">
                Este email foi enviado automaticamente. Não responda a este email.
            </p>
        </div>
        """

        message = MessageSchema(
            subject="Redefinir Senha - HireMetrics",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        # Send email
        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        print(f"Error sending password reset email: {e}")
        raise e


# Authentication is now handled in utils/auth_utils.py


# Routes
@app.post("/api/auth/register", response_model=schemas.RegistrationResponse)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create user with verification
    new_user = crud.create_user_with_verification(db=db, user=user)

    # Send verification email
    try:
        await send_verification_email(new_user.email, new_user.email_verification_token)
        return schemas.RegistrationResponse(
            success=True,
            message="Conta criada com sucesso! Verifique seu email para ativar sua conta.",
            user_id=new_user.id,
        )
    except Exception as e:
        # If email sending fails, still create the user but inform them
        print(f"Error sending verification email: {e}")
        return schemas.RegistrationResponse(
            success=True,
            message="Conta criada com sucesso! Houve um problema ao enviar o email de verificação. Entre em contato conosco.",
            user_id=new_user.id,
        )


@app.post("/api/auth/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if email is verified
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Email não verificado. Verifique seu email antes de fazer login.",
                "code": "EMAIL_NOT_VERIFIED",
                "email": user.email,
            },
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_user_token(user, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/auth/verify-email", response_model=schemas.EmailVerificationResponse)
async def verify_email(
    request: schemas.EmailVerificationRequest, db: Session = Depends(get_db)
):
    success, message = crud.verify_user_email(db, request.token)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return schemas.EmailVerificationResponse(success=True, message=message)


@app.post(
    "/api/auth/resend-verification", response_model=schemas.ResendVerificationResponse
)
async def resend_verification(
    request: schemas.ResendVerificationRequest, db: Session = Depends(get_db)
):
    success, message = crud.resend_verification_email(db, request.email)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    # Send new verification email
    user = crud.get_user_by_email(db, request.email)
    try:
        await send_verification_email(user.email, user.email_verification_token)
        return schemas.ResendVerificationResponse(success=True, message=message)
    except Exception as e:
        print(f"Error sending verification email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao enviar email de verificação. Tente novamente mais tarde.",
        )


@app.post("/api/auth/forgot-password", response_model=schemas.ForgotPasswordResponse)
async def forgot_password(
    request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)
):
    success, message = crud.request_password_reset(db, request.email)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    # Send password reset email
    user = crud.get_user_by_email(db, request.email)
    try:
        await send_password_reset_email(user.email, user.password_reset_token)
        return schemas.ForgotPasswordResponse(success=True, message=message)
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao enviar email de redefinição de senha. Tente novamente mais tarde.",
        )


@app.post("/api/auth/reset-password", response_model=schemas.ResetPasswordResponse)
async def reset_password(
    request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)
):
    success, message = crud.reset_user_password(db, request.token, request.new_password)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return schemas.ResetPasswordResponse(success=True, message=message)


@app.post(
    "/api/auth/validate-reset-token", response_model=schemas.ValidateResetTokenResponse
)
async def validate_reset_token(
    request: schemas.ValidateResetTokenRequest, db: Session = Depends(get_db)
):
    success, message = crud.validate_reset_token(db, request.token)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return schemas.ValidateResetTokenResponse(success=True, message=message)


@app.get("/api/auth/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# Google OAuth endpoints
@app.get("/api/auth/google/login")
async def google_login():
    """Initiate Google OAuth login"""
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")

    # Build Google OAuth URL
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    # Construct the authorization URL
    auth_url = f"{google_auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    return {"auth_url": auth_url}


@app.get("/api/auth/google/callback")
async def google_callback(
    code: Optional[str] = None,
    error: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Handle Google OAuth callback"""
    # Handle cancellation or error from Google
    if error:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        return RedirectResponse(
            url=f"{frontend_url}/auth/google-callback?error={error}"
        )

    # Check if code is provided
    if not code:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        return RedirectResponse(
            url=f"{frontend_url}/auth/google-callback?error=missing_code"
        )

    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        return RedirectResponse(
            url=f"{frontend_url}/auth/google-callback?error=oauth_not_configured"
        )

    try:
        # Exchange authorization code for access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        }

        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        token_info = token_response.json()

        # Get user info from Google
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {token_info['access_token']}"}
        user_response = requests.get(user_info_url, headers=headers)
        user_response.raise_for_status()
        google_user = user_response.json()

        # Check if user exists in our database
        user = crud.get_user_by_email(db, email=google_user["email"])

        if not user:
            # Create new user
            user_data = {
                "email": google_user["email"],
                "first_name": google_user.get("given_name", ""),
                "last_name": google_user.get("family_name", ""),
                "auth_provider": "google",
                "google_id": google_user["id"],
            }
            user = crud.create_oauth_user(db, user_data)
        else:
            # Update existing user with Google info if needed
            if not user.google_id:
                user.google_id = google_user["id"]
                user.auth_provider = "google"
                user.email_verified = True
                db.commit()
                db.refresh(user)

        # Update last_login timestamp
        user.last_login = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)

        # Create access token
        access_token = create_user_token(user)

        # Redirect to frontend with token
        frontend_url = settings.FRONTEND_URL
        return RedirectResponse(
            url=f"{frontend_url}/auth/google-callback?token={access_token}"
        )

    except requests.RequestException as e:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        error_msg = f"google_oauth_error: {str(e)}"
        return RedirectResponse(
            url=f"{frontend_url}/auth/google-callback?error={error_msg}"
        )
    except Exception as e:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        error_msg = f"authentication_error: {str(e)}"
        return RedirectResponse(
            url=f"{frontend_url}/auth/google-callback?error={error_msg}"
        )


@app.post("/api/auth/change-password", response_model=schemas.PasswordChangeResponse)
async def change_password(
    password_data: schemas.PasswordChange,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    success = crud.change_user_password(
        db,
        str(current_user.id),
        password_data.current_password,
        password_data.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Senha atual incorreta"
        )

    return schemas.PasswordChangeResponse(message="Senha alterada com sucesso!")


@app.put("/api/auth/preferences", response_model=schemas.UserPreferencesUpdate)
async def update_user_preferences(
    preferences: schemas.UserPreferencesUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    success = crud.update_user_preferences(db, str(current_user.id), preferences.dict())

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar preferências",
        )

    return preferences


@app.get("/api/dashboard/jobs", response_model=list[JobDashboardBase])
def get_job_dashboard_base(
    limit: int = Query(1000, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    job_posted_at_date: Optional[str] = Query(
        None, description="Filter by job posted date (YYYY-MM-DD)"
    ),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    job_city: Optional[str] = Query(None, description="Filter by job city"),
    job_state: Optional[str] = Query(None, description="Filter by job state"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 10000
        )
        validated_offset = SecureQueryBuilder.validate_integer_input(
            offset, "offset", 0
        )

        # Build secure filters
        filters = {}
        params = {"limit": validated_limit, "offset": validated_offset}

        # Validate date inputs
        if job_posted_at_date not in (None, "", "null"):
            validated_date = SecureQueryBuilder.validate_date_input(
                job_posted_at_date, "job_posted_at_date"
            )
            filters["job_posted_at_date >= :job_posted_at_date"] = validated_date
            params["job_posted_at_date"] = validated_date

        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters["job_posted_at_date >= :job_posted_at_date_from"] = (
                validated_date_from
            )
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters["job_posted_at_date <= :job_posted_at_date_to"] = validated_date_to
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if job_city not in (None, "", "null"):
            validated_city = SecureQueryBuilder.validate_text_input(
                job_city, "job_city"
            )
            filters["job_city ILIKE :job_city"] = validated_city
            params["job_city"] = f"%{validated_city}%"

        if job_state not in (None, "", "null"):
            validated_state = SecureQueryBuilder.validate_text_input(
                job_state, "job_state"
            )
            filters["job_state ILIKE :job_state"] = validated_state
            params["job_state"] = f"%{validated_state}%"

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            filters["job_is_remote = :job_is_remote"] = validated_remote
            params["job_is_remote"] = validated_remote

        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters["employer_name = :employer_name"] = validated_employer
            params["employer_name"] = validated_employer

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters["search_position_query = :search_position_query"] = (
                validated_position
            )
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters.keys())}" if filters else ""

        # Use parameterized query
        base_query = """
            SELECT job_id, job_title, job_employment_type, job_is_remote, job_posted_at_date, 
                   job_publisher, employer_name, job_city, job_state, apply_options, 
                   created_at, updated_at, created_by, updated_by
            FROM target.job_dashboard_base
        """

        full_query = f"{base_query} {where_clause} ORDER BY job_posted_at_date DESC LIMIT :limit OFFSET :offset"
        query = text(full_query)

        result = db.execute(query, params)
        jobs = result.mappings().all()
        return jobs

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/top-skills", response_model=list[TopSkill])
@cache_result(ttl=300, key_prefix="top_skills")  # Cache for 5 minutes
def get_top_skills(
    limit: int = Query(10, ge=1, le=1000),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 1000
        )

        # Build secure filters
        filters = {}
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters["job_posted_at_date >= :job_posted_at_date_from"] = (
                validated_date_from
            )
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters["job_posted_at_date <= :job_posted_at_date_to"] = validated_date_to
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters["seniority = :seniority"] = validated_seniority
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters["search_position_query = :search_position_query"] = (
                validated_position
            )
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters.keys())}" if filters else ""

        # Optimized query - avoid complex CTE and JOIN operations
        if seniority is None:
            # When no seniority filter, first get top skills by total count, then get all seniority levels for those skills
            # This ensures we get complete seniority breakdown for the top skills
            base_query = """
                WITH top_skills AS (
                    SELECT 
                        skill,
                        SUM(skill_count) as total_count
                    FROM target.job_skills
                    {where_clause}
                    GROUP BY skill
                    ORDER BY total_count DESC
                    LIMIT :limit
                )
                SELECT 
                    js.skill,
                    js.seniority,
                    SUM(js.skill_count) as skill_count,
                    MAX(ts.total_count) as total_count
                FROM target.job_skills js
                INNER JOIN top_skills ts ON js.skill = ts.skill
                {where_clause}
                GROUP BY js.skill, js.seniority
                ORDER BY total_count DESC, js.skill, skill_count DESC
            """
            full_query = base_query.format(where_clause=where_clause)
        else:
            # If seniority is specified, include seniority field for API consistency
            base_query = """
                SELECT skill, seniority, SUM(skill_count) as skill_count
                FROM target.job_skills
                {where_clause}
                GROUP BY skill, seniority
                ORDER BY skill_count DESC
                LIMIT :limit
            """
            full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        skills = result.mappings().all()

        return skills

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Error in top-skills endpoint: {e}")
        if "timeout" in str(e).lower() or "connection" in str(e).lower():
            raise HTTPException(
                status_code=503,
                detail="Database temporarily unavailable. Please try again.",
            )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/skills-trend")
def get_skills_trend(
    request: Request,
    limit: int = Query(
        50, ge=1, le=100
    ),  # Increased from 5,20 to 50,100 to allow more skills for chart
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 100
        )

        # Build secure filters
        filters = {}
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters["job_posted_at_date >= :job_posted_at_date_from"] = (
                validated_date_from
            )
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters["job_posted_at_date <= :job_posted_at_date_to"] = validated_date_to
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters["seniority = :seniority"] = validated_seniority
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters["search_position_query = :search_position_query"] = (
                validated_position
            )
            params["search_position_query"] = validated_position

        # Extract and validate skills from query parameters
        skills = []
        query_params = dict(request.query_params)

        # Handle both skills[] and skills parameters
        if "skills[]" in query_params:
            skills_param = query_params["skills[]"]
            if isinstance(skills_param, str):
                skills = [skills_param]
            else:
                skills = skills_param
        elif "skills" in query_params:
            skills_param = query_params["skills"]
            if isinstance(skills_param, str):
                skills = [skills_param]
            else:
                skills = skills_param

        # Also check for multiple skills[] parameters
        for key, value in request.query_params.multi_items():
            if key == "skills[]":
                if value not in skills:
                    skills.append(value)
            elif key == "skills":
                if value not in skills:
                    skills.append(value)

        # Handle skills filtering with validation
        if skills and len(skills) > 0:
            # Filter out empty strings and None values, then validate
            valid_skills = []
            for skill in skills:
                if skill and skill.strip():
                    validated_skill = SecureQueryBuilder.validate_text_input(
                        skill, "skill"
                    )
                    valid_skills.append(validated_skill)

            if valid_skills:
                # Create dynamic placeholders for IN clause
                skill_placeholders = ", ".join(
                    [f":skill_{i}" for i in range(len(valid_skills))]
                )
                filters[f"skill IN ({skill_placeholders})"] = valid_skills
                for i, skill in enumerate(valid_skills):
                    params[f"skill_{i}"] = skill
        else:
            # Get top N skills if not provided
            where_clause_for_top = (
                f"WHERE {' AND '.join(filters.keys())}" if filters else ""
            )
            top_skills_query = text(
                f"""
                SELECT skill
                FROM target.job_skills
                {where_clause_for_top}
                GROUP BY skill
                ORDER BY SUM(skill_count) DESC
                LIMIT :limit
            """
            )
            params_for_top = {**params, "limit": validated_limit}
            result = db.execute(top_skills_query, params_for_top)
            top_skills = [row[0] for row in result]

            if top_skills:
                # Create dynamic placeholders for IN clause
                skill_placeholders = ", ".join(
                    [f":skill_{i}" for i in range(len(top_skills))]
                )
                filters[f"skill IN ({skill_placeholders})"] = top_skills
                for i, skill in enumerate(top_skills):
                    params[f"skill_{i}"] = skill

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters.keys())}" if filters else ""

        # Use parameterized query
        base_query = """
            SELECT 
                job_posted_at_date,
                skill,
                seniority,
                SUM(skill_count) as skill_count
            FROM target.job_skills
            {where_clause}
            GROUP BY job_posted_at_date, skill, seniority
            ORDER BY job_posted_at_date, skill, seniority
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        trends = result.mappings().all()
        return trends

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Error in skills-trend endpoint: {e}")
        if "timeout" in str(e).lower() or "connection" in str(e).lower():
            raise HTTPException(
                status_code=503,
                detail="Database temporarily unavailable. Please try again.",
            )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/available-skills", response_model=list[str])
@cache_result(ttl=600, key_prefix="available_skills")  # Cache for 10 minutes
def get_available_skills(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of all available skills from the database.
    """
    try:
        # Build secure filters
        filters = {}
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters["search_position_query = :search_position_query"] = (
                validated_position
            )
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters.keys())}" if filters else ""

        # Use parameterized query
        base_query = """
            SELECT DISTINCT skill
            FROM target.job_skills
            {where_clause}
            ORDER BY skill
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        skills = [row[0] for row in result]
        return skills

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/available-seniority-levels", response_model=list[str])
@cache_result(ttl=600, key_prefix="available_seniority")  # Cache for 10 minutes
def get_available_seniority_levels(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of all available seniority levels from the database.
    """
    try:
        # Build secure filters
        filters = ["seniority IS NOT NULL AND seniority != ''"]
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}"

        # Use parameterized query
        base_query = """
            SELECT DISTINCT seniority
            FROM target.job_skills
            {where_clause}
            ORDER BY seniority DESC
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        seniority_levels = [row[0] for row in result]
        return seniority_levels

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/available-positions", response_model=list[str])
@cache_result(ttl=1800, key_prefix="available_positions")  # Cache for 30 minutes
def get_available_positions(db: Session = Depends(get_db)):
    """
    Get list of all available positions from the database.
    """
    try:
        # Use parameterized query (no user input, so safe)
        query = text(
            """
            SELECT DISTINCT search_position_query
            FROM target.job_dashboard_base
            WHERE search_position_query IS NOT NULL AND search_position_query != ''
            ORDER BY search_position_query
        """
        )

        result = db.execute(query)
        positions = [row[0] for row in result]
        return positions

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/locations", response_model=list[dict])
def get_filtered_locations(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    db: Session = Depends(get_db),
):
    """
    Get filtered city/state locations based on position and date filters.
    """
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Use parameterized query
        base_query = """
            SELECT DISTINCT job_city, job_state
            FROM target.job_dashboard_base
            {where_clause}
            AND job_city IS NOT NULL AND job_city != ''
            AND job_state IS NOT NULL AND job_state != ''
            ORDER BY job_city, job_state
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        locations = [
            {"title": row[0], "state": row[1]} for row in result if row[0] and row[1]
        ]
        return locations

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/available-publishers", response_model=list[str])
@cache_result(ttl=600, key_prefix="available_publishers")  # Cache for 10 minutes
def get_available_publishers(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of all available publishers from the database.
    """
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Use parameterized query
        base_query = """
            WITH expanded_options AS (
                SELECT DISTINCT (jsonb_array_elements(apply_options::jsonb) ->> 'publisher') as publisher
                FROM target.job_dashboard_base
                {where_clause}
            )
            SELECT publisher
            FROM expanded_options
            WHERE publisher IS NOT NULL AND publisher != ''
            ORDER BY publisher
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        publishers = [row[0] for row in result]
        return publishers

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/available-companies", response_model=list[str])
@cache_result(ttl=600, key_prefix="available_companies")  # Cache for 10 minutes
def get_available_companies(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of all available companies from the database.
    """
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        if filters:
            where_clause = f"WHERE {' AND '.join(filters)} AND employer_name IS NOT NULL AND employer_name != ''"
        else:
            where_clause = "WHERE employer_name IS NOT NULL AND employer_name != ''"

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Add job platform exclusion logic
        if job_platforms:
            # Create regex pattern for case-insensitive matching
            platform_patterns = []
            for platform in job_platforms:
                # Escape special regex characters and create case-insensitive pattern
                escaped_platform = (
                    platform.replace("\\", "\\\\")
                    .replace(".", "\\.")
                    .replace("*", "\\*")
                    .replace("+", "\\+")
                    .replace("?", "\\?")
                    .replace("^", "\\^")
                    .replace("$", "\\$")
                    .replace("[", "\\[")
                    .replace("]", "\\]")
                    .replace("(", "\\(")
                    .replace(")", "\\)")
                    .replace("|", "\\|")
                )
                platform_patterns.append(
                    f"LOWER(employer_name) NOT LIKE LOWER('%{escaped_platform}%')"
                )

            # Add the exclusion condition to the WHERE clause
            if where_clause:
                where_clause = where_clause.replace(
                    "WHERE", f"WHERE {' AND '.join(platform_patterns)} AND"
                )
            else:
                where_clause = f"WHERE {' AND '.join(platform_patterns)}"

        # Use parameterized query
        base_query = """
            SELECT DISTINCT employer_name
            FROM target.job_dashboard_base
            {where_clause}
            ORDER BY employer_name
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        companies = [row[0] for row in result]
        return companies

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"Error in get_available_companies: {str(e)}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


# Companies Analytics Endpoints


@app.get("/api/dashboard/top-companies")
@cache_result(ttl=300, key_prefix="top_companies")  # Cache for 5 minutes
def get_top_companies(
    limit: int = Query(20, ge=1, le=100),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get top companies by job count.
    """
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 100
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Use JOIN approach for job platform exclusion
        if job_platforms:
            # Create a CTE for job platforms to exclude
            platform_cte = """
            WITH job_platforms_to_exclude AS (
                SELECT DISTINCT job_publisher as platform_name
                FROM target.job_dashboard_base
                WHERE is_job_platform = true
                AND job_publisher IS NOT NULL
                AND job_publisher != ''
            )
            SELECT 
                jdb.employer_name,
                COUNT(jdb.job_id) as job_count
            FROM target.job_dashboard_base jdb
            LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
            {where_clause}
            AND jpe.platform_name IS NULL
            GROUP BY jdb.employer_name
            ORDER BY job_count DESC
            LIMIT :limit
            """
            full_query = platform_cte.format(where_clause=where_clause)
        else:
            # No job platforms to exclude, use simple approach
            base_query = """
                SELECT 
                    employer_name,
                    COUNT(job_id) as job_count
                FROM target.job_dashboard_base
                {where_clause}
                GROUP BY employer_name
                ORDER BY job_count DESC
                LIMIT :limit
            """
            full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        companies = result.mappings().all()
        return companies

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/companies-seniority-distribution")
def get_companies_seniority_distribution(
    limit: int = Query(10, ge=1, le=50),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get seniority distribution by top companies.
    """
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 50
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Add job platform exclusion logic
        if job_platforms:
            # Create regex pattern for case-insensitive matching
            platform_patterns = []
            for platform in job_platforms:
                # Escape special regex characters and create case-insensitive pattern
                escaped_platform = (
                    platform.replace("\\", "\\\\")
                    .replace(".", "\\.")
                    .replace("*", "\\*")
                    .replace("+", "\\+")
                    .replace("?", "\\?")
                    .replace("^", "\\^")
                    .replace("$", "\\$")
                    .replace("[", "\\[")
                    .replace("]", "\\]")
                    .replace("(", "\\(")
                    .replace(")", "\\)")
                    .replace("|", "\\|")
                )
                platform_patterns.append(
                    f"LOWER(employer_name) NOT LIKE LOWER('%{escaped_platform}%')"
                )

            # Add the exclusion condition to the WHERE clause
            if where_clause:
                where_clause = where_clause.replace(
                    "WHERE", f"WHERE {' AND '.join(platform_patterns)} AND"
                )
            else:
                where_clause = f"WHERE {' AND '.join(platform_patterns)}"

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # If filtering by a specific company, simplify the query
        if employer_name not in (None, "", "null"):
            # Build additional filters excluding employer_name
            additional_filters = [
                f for f in filters if not f.startswith("employer_name")
            ]
            additional_where = (
                f"AND {' AND '.join(additional_filters)}" if additional_filters else ""
            )

            base_query = """
                SELECT 
                    employer_name,
                    seniority,
                    COUNT(job_id) as job_count
                FROM target.job_dashboard_base
                WHERE employer_name = :employer_name
                {additional_where}
                GROUP BY employer_name, seniority
                ORDER BY employer_name, seniority DESC
            """
            full_query = base_query.format(additional_where=additional_where)
        else:
            # Build WHERE clause for the main query
            main_where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

            # Use LEFT JOIN to exclude job platforms
            if job_platforms:
                # Create a CTE for job platforms to exclude
                platform_cte = """
                WITH job_platforms_to_exclude AS (
                    SELECT DISTINCT job_publisher as platform_name
                    FROM target.job_dashboard_base
                    WHERE is_job_platform = true
                    AND job_publisher IS NOT NULL
                    AND job_publisher != ''
                ),
                top_companies AS (
                    SELECT jdb.employer_name
                    FROM target.job_dashboard_base jdb
                    LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                    {main_where_clause}
                    AND jpe.platform_name IS NULL
                    GROUP BY jdb.employer_name
                    ORDER BY COUNT(jdb.job_id) DESC
                    LIMIT :limit
                )
                SELECT 
                    jdb.employer_name,
                    jdb.seniority,
                    COUNT(jdb.job_id) as job_count
                FROM target.job_dashboard_base jdb
                INNER JOIN top_companies tc ON jdb.employer_name = tc.employer_name
                LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                {main_where_clause}
                AND jpe.platform_name IS NULL
                GROUP BY jdb.employer_name, jdb.seniority
                ORDER BY jdb.employer_name, jdb.seniority DESC
                """
                full_query = platform_cte.format(main_where_clause=main_where_clause)
            else:
                # No job platforms to exclude, use simple approach
                base_query = """
                WITH top_companies AS (
                    SELECT employer_name
                    FROM target.job_dashboard_base
                    {main_where_clause}
                    GROUP BY employer_name
                    ORDER BY COUNT(job_id) DESC
                    LIMIT :limit
                )
                SELECT 
                    jdb.employer_name,
                    jdb.seniority,
                    COUNT(jdb.job_id) as job_count
                FROM target.job_dashboard_base jdb
                INNER JOIN top_companies tc ON jdb.employer_name = tc.employer_name
                {main_where_clause}
                GROUP BY jdb.employer_name, jdb.seniority
                ORDER BY jdb.employer_name, jdb.seniority DESC
                """
                full_query = base_query.format(main_where_clause=main_where_clause)

        try:
            query = text(full_query)
            result = db.execute(query, params)
            distribution = result.mappings().all()
            return distribution
        except Exception as e:
            raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/employment-type-distribution")
def get_employment_type_distribution(
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get employment type distribution.
    """
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # If filtering by a specific company, simplify the query
        if employer_name not in (None, "", "null"):
            # Build additional filters excluding employer_name
            additional_filters = [
                f for f in filters if not f.startswith("employer_name")
            ]
            additional_where = (
                f"AND {' AND '.join(additional_filters)}" if additional_filters else ""
            )

            base_query = """
                SELECT 
                    job_employment_type,
                    COUNT(job_id) as job_count,
                    ROUND(COUNT(job_id) * 100.0 / SUM(COUNT(job_id)) OVER (), 2) as percentage
                FROM target.job_dashboard_base
                WHERE employer_name = :employer_name
                {additional_where}
                GROUP BY job_employment_type
                ORDER BY job_count DESC
            """
            full_query = base_query.format(additional_where=additional_where)
        else:
            base_query = """
                SELECT 
                    job_employment_type,
                    COUNT(job_id) as job_count,
                    ROUND(COUNT(job_id) * 100.0 / SUM(COUNT(job_id)) OVER (), 2) as percentage
                FROM target.job_dashboard_base
                {where_clause}
                GROUP BY job_employment_type
                ORDER BY job_count DESC
            """
            full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        distribution = result.mappings().all()
        return distribution

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/companies-remote-percentage")
def get_companies_remote_percentage(
    limit: int = Query(20, ge=1, le=100),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get remote job percentage by company.
    """
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 100
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Use JOIN approach for job platform exclusion
        if job_platforms:
            # Create a CTE for job platforms to exclude
            platform_cte = """
            WITH job_platforms_to_exclude AS (
                SELECT DISTINCT job_publisher as platform_name
                FROM target.job_dashboard_base
                WHERE is_job_platform = true
                AND job_publisher IS NOT NULL
                AND job_publisher != ''
            )
            """

            # If filtering by a specific company, job_is_remote, or seniority, don't filter by minimum job count
            if (
                employer_name not in (None, "", "null")
                or job_is_remote not in (None, "", "null")
                or seniority not in (None, "", "null")
            ):
                base_query = """
                {platform_cte}
                SELECT 
                    jdb.employer_name,
                    COUNT(jdb.job_id) as total_jobs,
                    SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) as remote_jobs,
                    ROUND(
                        SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) * 100.0 / COUNT(jdb.job_id), 
                        2
                    ) as remote_percentage
                FROM target.job_dashboard_base jdb
                LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                {where_clause}
                AND jpe.platform_name IS NULL
                GROUP BY jdb.employer_name
                ORDER BY remote_percentage DESC, total_jobs DESC
                LIMIT :limit
                """
                full_query = base_query.format(
                    platform_cte=platform_cte, where_clause=where_clause
                )
            else:
                # Modified logic: Show companies with remote jobs or companies with at least 2 jobs
                base_query = """
                {platform_cte}
                SELECT 
                    jdb.employer_name,
                    COUNT(jdb.job_id) as total_jobs,
                    SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) as remote_jobs,
                    ROUND(
                        SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) * 100.0 / COUNT(jdb.job_id), 
                        2
                    ) as remote_percentage
                FROM target.job_dashboard_base jdb
                LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                {where_clause}
                AND jpe.platform_name IS NULL
                GROUP BY jdb.employer_name
                HAVING COUNT(jdb.job_id) >= 2 OR SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) > 0
                ORDER BY remote_percentage DESC, total_jobs DESC
                LIMIT :limit
                """
                full_query = base_query.format(
                    platform_cte=platform_cte, where_clause=where_clause
                )
        else:
            # No job platforms to exclude, use simple approach
            if (
                employer_name not in (None, "", "null")
                or job_is_remote not in (None, "", "null")
                or seniority not in (None, "", "null")
            ):
                base_query = """
                    SELECT 
                        employer_name,
                        COUNT(job_id) as total_jobs,
                        SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) as remote_jobs,
                        ROUND(
                            SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) * 100.0 / COUNT(job_id), 
                            2
                        ) as remote_percentage
                    FROM target.job_dashboard_base
                    {where_clause}
                    GROUP BY employer_name
                    ORDER BY remote_percentage DESC, total_jobs DESC
                    LIMIT :limit
                """
                full_query = base_query.format(where_clause=where_clause)
            else:
                # Modified logic: Show companies with remote jobs or companies with at least 2 jobs
                base_query = """
                    SELECT 
                        employer_name,
                        COUNT(job_id) as total_jobs,
                        SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) as remote_jobs,
                        ROUND(
                            SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) * 100.0 / COUNT(job_id), 
                            2
                        ) as remote_percentage
                    FROM target.job_dashboard_base
                    {where_clause}
                    GROUP BY employer_name
                    HAVING COUNT(job_id) >= 2 OR SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) > 0
                    ORDER BY remote_percentage DESC, total_jobs DESC
                    LIMIT :limit
                """
                full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        remote_stats = result.mappings().all()
        return remote_stats

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/companies-jobs-timeline")
def get_companies_jobs_timeline(
    limit: int = Query(5, ge=1, le=20),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get jobs timeline by top companies.
    """
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 20
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Add job platform exclusion logic
        if job_platforms:
            # Create regex pattern for case-insensitive matching
            platform_patterns = []
            for platform in job_platforms:
                # Escape special regex characters and create case-insensitive pattern
                escaped_platform = (
                    platform.replace("\\", "\\\\")
                    .replace(".", "\\.")
                    .replace("*", "\\*")
                    .replace("+", "\\+")
                    .replace("?", "\\?")
                    .replace("^", "\\^")
                    .replace("$", "\\$")
                    .replace("[", "\\[")
                    .replace("]", "\\]")
                    .replace("(", "\\(")
                    .replace(")", "\\)")
                    .replace("|", "\\|")
                )
                platform_patterns.append(
                    f"LOWER(employer_name) NOT LIKE LOWER('%{escaped_platform}%')"
                )

            # Add the exclusion condition to the WHERE clause
            if where_clause:
                where_clause = where_clause.replace(
                    "WHERE", f"WHERE {' AND '.join(platform_patterns)} AND"
                )
            else:
                where_clause = f"WHERE {' AND '.join(platform_patterns)}"

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # If filtering by a specific company, simplify the query
        if employer_name not in (None, "", "null"):
            # Build additional filters excluding employer_name
            additional_filters = [
                f for f in filters if not f.startswith("employer_name")
            ]
            additional_where = (
                f"AND {' AND '.join(additional_filters)}" if additional_filters else ""
            )

            base_query = """
                SELECT 
                    job_posted_at_date,
                    employer_name,
                    COUNT(job_id) as job_count
                FROM target.job_dashboard_base
                WHERE employer_name = :employer_name
                {additional_where}
                GROUP BY job_posted_at_date, employer_name
                ORDER BY job_posted_at_date, employer_name
            """
            full_query = base_query.format(additional_where=additional_where)
        else:
            # Build WHERE clause for the main query
            main_where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

            # Use LEFT JOIN to exclude job platforms
            if job_platforms:
                # Create a CTE for job platforms to exclude
                platform_cte = """
                WITH job_platforms_to_exclude AS (
                    SELECT DISTINCT job_publisher as platform_name
                    FROM target.job_dashboard_base
                    WHERE is_job_platform = true
                    AND job_publisher IS NOT NULL
                    AND job_publisher != ''
                ),
                top_companies AS (
                    SELECT jdb.employer_name
                    FROM target.job_dashboard_base jdb
                    LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                    {main_where_clause}
                    AND jpe.platform_name IS NULL
                    GROUP BY jdb.employer_name
                    ORDER BY COUNT(jdb.job_id) DESC
                    LIMIT :limit
                )
                SELECT 
                    jdb.job_posted_at_date,
                    jdb.employer_name,
                    COUNT(jdb.job_id) as job_count
                FROM target.job_dashboard_base jdb
                INNER JOIN top_companies tc ON jdb.employer_name = tc.employer_name
                LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                {main_where_clause}
                AND jpe.platform_name IS NULL
                GROUP BY jdb.job_posted_at_date, jdb.employer_name
                ORDER BY jdb.job_posted_at_date, jdb.employer_name
                """
                full_query = platform_cte.format(main_where_clause=main_where_clause)
            else:
                # No job platforms to exclude, use simple approach
                base_query = """
                WITH top_companies AS (
                    SELECT employer_name
                    FROM target.job_dashboard_base
                    {main_where_clause}
                    GROUP BY employer_name
                    ORDER BY COUNT(job_id) DESC
                    LIMIT :limit
                )
                SELECT 
                    jdb.job_posted_at_date,
                    jdb.employer_name,
                    COUNT(jdb.job_id) as job_count
                FROM target.job_dashboard_base jdb
                INNER JOIN top_companies tc ON jdb.employer_name = tc.employer_name
                {main_where_clause}
                GROUP BY jdb.job_posted_at_date, jdb.employer_name
                ORDER BY jdb.job_posted_at_date, jdb.employer_name
                """
                full_query = base_query.format(main_where_clause=main_where_clause)

        try:
            query = text(full_query)
            result = db.execute(query, params)
            timeline = result.mappings().all()
            return timeline
        except Exception as e:
            raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/companies-top-skills")
def get_companies_top_skills(
    limit: int = Query(10, ge=1, le=50),
    skills_limit: int = Query(10, ge=5, le=50),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get top skills by company with word cloud format data.
    """
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 50
        )
        validated_skills_limit = SecureQueryBuilder.validate_integer_input(
            skills_limit, "skills_limit", 5, 50
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit, "skills_limit": validated_skills_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # If filtering by a specific company, simplify the query
        if employer_name not in (None, "", "null"):
            # Build additional filters excluding employer_name
            additional_filters = [
                f for f in filters if not f.startswith("employer_name")
            ]
            additional_where = (
                f"AND {' AND '.join(additional_filters)}" if additional_filters else ""
            )

            base_query = """
                WITH skills_extracted AS (
                    SELECT 
                        jsonb_array_elements_text(extracted_skills::jsonb) as skill
                    FROM target.job_dashboard_base
                    WHERE employer_name = :employer_name
                    AND extracted_skills IS NOT NULL
                    AND extracted_skills::jsonb != '[]'::jsonb
                    {additional_where}
                )
                SELECT 
                    skill as name,
                    COUNT(*) as value
                FROM skills_extracted
                GROUP BY skill
                ORDER BY value DESC
                LIMIT :skills_limit
            """
            full_query = base_query.format(additional_where=additional_where)
        else:
            # For all companies or filtered subset - optimized version
            base_query = """
                WITH company_skills AS (
                    SELECT 
                        jsonb_array_elements_text(extracted_skills::jsonb) as skill
                    FROM target.job_dashboard_base
                    {where_clause}
                    AND extracted_skills IS NOT NULL
                    AND extracted_skills::jsonb != '[]'::jsonb
                    AND employer_name IN (
                        SELECT employer_name
                        FROM target.job_dashboard_base
                        {where_clause}
                        GROUP BY employer_name
                        ORDER BY COUNT(*) DESC
                        LIMIT :limit
                    )
                )
                SELECT 
                    skill as name,
                    COUNT(*) as value
                FROM company_skills
                GROUP BY skill
                ORDER BY value DESC
                LIMIT :skills_limit
            """
            full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        skills = result.mappings().all()
        return list(skills)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/companies-kpis")
def get_companies_kpis(
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get KPIs for companies: total job postings, % remote jobs, average skills per job.
    """
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Total job postings
        total_jobs_base_query = """
            SELECT COUNT(DISTINCT job_id) as total_jobs
            FROM target.job_dashboard_base
            {where_clause}
        """
        total_jobs_query = text(total_jobs_base_query.format(where_clause=where_clause))

        # Percentage of remote jobs
        remote_percentage_base_query = """
            SELECT 
                ROUND(
                    (COUNT(DISTINCT job_id) FILTER (WHERE job_is_remote = true) * 100.0 / 
                     NULLIF(COUNT(DISTINCT job_id), 0)), 2
                ) as remote_percentage
            FROM target.job_dashboard_base
            {where_clause}
        """
        remote_percentage_query = text(
            remote_percentage_base_query.format(where_clause=where_clause)
        )

        # Average skills per job
        avg_skills_base_query = """
            SELECT 
                ROUND(AVG(skills_per_job), 2) as avg_skills_per_job
            FROM (
                SELECT 
                    job_id,
                    COALESCE(jsonb_array_length(extracted_skills::jsonb), 0) as skills_per_job
                FROM target.job_dashboard_base
                WHERE extracted_skills IS NOT NULL
                {additional_where}
            ) job_skill_counts
        """
        additional_where = f"AND {' AND '.join(filters)}" if filters else ""
        avg_skills_query = text(
            avg_skills_base_query.format(additional_where=additional_where)
        )

        # Count of distinct companies
        distinct_companies_base_query = """
            SELECT COUNT(DISTINCT employer_name) as distinct_companies
            FROM target.job_dashboard_base
            WHERE employer_name IS NOT NULL
            {additional_where}
        """
        distinct_companies_query = text(
            distinct_companies_base_query.format(additional_where=additional_where)
        )

        total_jobs_result = db.execute(total_jobs_query, params).fetchone()
        remote_percentage_result = db.execute(
            remote_percentage_query, params
        ).fetchone()
        avg_skills_result = db.execute(avg_skills_query, params).fetchone()
        distinct_companies_result = db.execute(
            distinct_companies_query, params
        ).fetchone()

        return {
            "total_jobs": total_jobs_result[0] if total_jobs_result else 0,
            "remote_percentage": (
                float(remote_percentage_result[0] or 0)
                if remote_percentage_result
                else 0
            ),
            "avg_skills_per_job": (
                float(avg_skills_result[0] or 0) if avg_skills_result else 0
            ),
            "distinct_companies": (
                distinct_companies_result[0] if distinct_companies_result else 0
            ),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# Publishers Analytics Endpoints


@app.get("/api/dashboard/publishers-kpis")
def get_publishers_kpis(
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get KPIs for publishers: total publishers, avg per job, biggest coverage, % direct applications.
    """
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        # Total unique publishers
        total_publishers_base_query = """
            WITH publishers_extracted AS (
                SELECT DISTINCT (jsonb_array_elements(apply_options::jsonb) ->> 'publisher') as publisher
                FROM target.job_dashboard_base
                {where_clause}
            )
            SELECT COUNT(*) as total_publishers
            FROM publishers_extracted
            {publisher_filter}
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        total_publishers_query = text(
            total_publishers_base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        # Average publishers per job
        avg_publishers_base_query = """
            SELECT 
                AVG(jsonb_array_length(apply_options::jsonb)) as avg_publishers_per_job
            FROM target.job_dashboard_base
            {where_clause}
        """
        avg_publishers_query = text(
            avg_publishers_base_query.format(where_clause=where_clause)
        )

        # Publisher with biggest coverage (filtered by publisher if specified)
        biggest_coverage_base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher
                FROM target.job_dashboard_base
                {where_clause}
            ),
            publisher_coverage AS (
                SELECT 
                    publisher,
                    COUNT(DISTINCT job_id) as job_count
                FROM expanded_options
                {publisher_filter}
                GROUP BY publisher
            )
            SELECT publisher, job_count
            FROM publisher_coverage
            ORDER BY job_count DESC
            LIMIT 1
        """
        biggest_coverage_query = text(
            biggest_coverage_base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        # Percentage of direct applications
        direct_percentage_base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) as option
                FROM target.job_dashboard_base
                {where_clause}
            ),
            {filtered_options_cte}
            direct_stats AS (
                SELECT 
                    job_id,
                    BOOL_OR((option ->> 'is_direct')::boolean) as has_direct
                FROM {source_table}
                GROUP BY job_id
            )
            SELECT 
                CASE 
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE ROUND(
                        (COUNT(*) FILTER (WHERE has_direct = true) * 100.0 / COUNT(*)), 2
                    )
                END as direct_percentage
            FROM direct_stats
        """

        if publisher not in (None, "", "null"):
            filtered_options_cte = "filtered_options AS (SELECT job_id, option FROM expanded_options WHERE option ->> 'publisher' = :publisher),"
            source_table = "filtered_options"
        else:
            filtered_options_cte = ""
            source_table = "expanded_options"

        direct_percentage_query = text(
            direct_percentage_base_query.format(
                where_clause=where_clause,
                filtered_options_cte=filtered_options_cte,
                source_table=source_table,
            )
        )

        total_publishers_result = db.execute(total_publishers_query, params).fetchone()
        avg_publishers_result = db.execute(avg_publishers_query, params).fetchone()
        biggest_coverage_result = db.execute(biggest_coverage_query, params).fetchone()
        direct_percentage_result = db.execute(
            direct_percentage_query, params
        ).fetchone()

        return {
            "total_publishers": (
                total_publishers_result[0] if total_publishers_result else 0
            ),
            "avg_publishers_per_job": (
                round(float(avg_publishers_result[0] or 0), 2)
                if avg_publishers_result
                else 0
            ),
            "biggest_coverage_publisher": (
                biggest_coverage_result[0] if biggest_coverage_result else None
            ),
            "biggest_coverage_count": (
                biggest_coverage_result[1] if biggest_coverage_result else 0
            ),
            "direct_percentage": (
                float(direct_percentage_result[0] or 0)
                if direct_percentage_result
                else 0
            ),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/top-publishers")
@cache_result(ttl=300, key_prefix="top_publishers")  # Cache for 5 minutes
def get_top_publishers(
    limit: int = Query(20, ge=1, le=100),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get top publishers by volume of publications.
    """
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 100
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher
                FROM target.job_dashboard_base
                {where_clause}
            )
            SELECT 
                publisher,
                COUNT(*) as publication_count,
                COUNT(DISTINCT job_id) as unique_jobs_count
            FROM expanded_options
            {publisher_filter}
            GROUP BY publisher
            ORDER BY unique_jobs_count DESC
            LIMIT :limit
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        query = text(
            base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        result = db.execute(query, params)
        publishers = result.mappings().all()
        return publishers

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/publishers-seniority-distribution")
def get_publishers_seniority_distribution(
    limit: int = Query(10, ge=1, le=50),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get seniority distribution by top publishers.
    """
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 50
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher
                FROM target.job_dashboard_base
                {where_clause}
            ),
            top_publishers AS (
                SELECT 
                    publisher,
                    COUNT(*) as total_count
                FROM expanded_options
                {publisher_filter}
                GROUP BY publisher
                ORDER BY total_count DESC
                LIMIT :limit
            ),
            publisher_seniority AS (
                SELECT DISTINCT
                    eo.publisher,
                    jdb.seniority,
                    eo.job_id
                FROM expanded_options eo
                INNER JOIN target.job_dashboard_base jdb ON eo.job_id = jdb.job_id
                INNER JOIN top_publishers tp ON eo.publisher = tp.publisher
            )
            SELECT 
                publisher,
                seniority,
                COUNT(job_id) as job_count
            FROM publisher_seniority
            WHERE seniority IS NOT NULL
            GROUP BY publisher, seniority
            ORDER BY publisher, seniority DESC
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        query = text(
            base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        result = db.execute(query, params)
        distribution = result.mappings().all()
        return distribution

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/publishers-companies-matrix")
def get_publishers_companies_matrix(
    limit_publishers: int = Query(15, ge=5, le=50),
    limit_companies: int = Query(15, ge=5, le=50),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get publisher × company usage matrix.
    """
    try:
        # Validate and sanitize inputs
        validated_limit_publishers = SecureQueryBuilder.validate_integer_input(
            limit_publishers, "limit_publishers", 5, 50
        )
        validated_limit_companies = SecureQueryBuilder.validate_integer_input(
            limit_companies, "limit_companies", 5, 50
        )

        # Build secure filters
        filters = []
        params = {
            "limit_publishers": validated_limit_publishers,
            "limit_companies": validated_limit_companies,
        }

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        # Optimized query with better structure and reduced CTEs
        base_query = """
            WITH publisher_counts AS (
                SELECT 
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher,
                    COUNT(*) as total_count
                FROM target.job_dashboard_base
                {where_clause}
                AND apply_options IS NOT NULL
                AND apply_options::jsonb != '[]'::jsonb
                {publisher_filter}
                GROUP BY jsonb_array_elements(apply_options::jsonb) ->> 'publisher'
                ORDER BY total_count DESC
                LIMIT :limit_publishers
            ),
            company_counts AS (
                SELECT 
                    employer_name,
                    COUNT(*) as total_count
                FROM target.job_dashboard_base
                {where_clause}
                GROUP BY employer_name
                ORDER BY total_count DESC
                LIMIT :limit_companies
            ),
            matrix_data AS (
                SELECT 
                    jsonb_array_elements(jdb.apply_options::jsonb) ->> 'publisher' as publisher,
                    jdb.employer_name,
                    jdb.job_id
                FROM target.job_dashboard_base jdb
                INNER JOIN company_counts cc ON jdb.employer_name = cc.employer_name
                {where_clause}
                AND jdb.apply_options IS NOT NULL
                AND jdb.apply_options::jsonb != '[]'::jsonb
            )
            SELECT 
                md.publisher,
                md.employer_name,
                COUNT(md.job_id) as job_count
            FROM matrix_data md
            INNER JOIN publisher_counts pc ON md.publisher = pc.publisher
            GROUP BY md.publisher, md.employer_name
            ORDER BY md.publisher, md.employer_name
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        query = text(
            base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        result = db.execute(query, params)
        matrix = result.mappings().all()
        return matrix

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/publishers-timeline")
def get_publishers_timeline(
    limit: int = Query(10, ge=1, le=20),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get publishers timeline data.
    """
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 20
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    job_posted_at_date,
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher
                FROM target.job_dashboard_base
                {where_clause}
            ),
            top_publishers AS (
                SELECT 
                    publisher,
                    COUNT(*) as total_count
                FROM expanded_options
                {publisher_filter}
                GROUP BY publisher
                ORDER BY total_count DESC
                LIMIT :limit
            ),
            publisher_timeline AS (
                SELECT DISTINCT
                    eo.job_posted_at_date,
                    eo.publisher,
                    eo.job_id
                FROM expanded_options eo
                INNER JOIN top_publishers tp ON eo.publisher = tp.publisher
            )
            SELECT 
                job_posted_at_date,
                publisher,
                COUNT(job_id) as job_count
            FROM publisher_timeline
            GROUP BY job_posted_at_date, publisher
            ORDER BY job_posted_at_date, publisher
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        query = text(
            base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        result = db.execute(query, params)
        timeline = result.mappings().all()
        return timeline

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/dashboard/direct-vs-indirect-distribution")
def get_direct_vs_indirect_distribution(
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get direct vs indirect application distribution.
    """
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) as option
                FROM target.job_dashboard_base
                {where_clause}
            ),
            {filtered_options_cte}
            application_types AS (
                SELECT 
                    (option ->> 'is_direct')::boolean as is_direct,
                    COUNT(*) as count
                FROM {source_table}
                GROUP BY is_direct
            )
            SELECT 
                CASE WHEN is_direct THEN 'Direct' ELSE 'Indirect' END as application_type,
                count,
                ROUND(count * 100.0 / SUM(count) OVER (), 2) as percentage
            FROM application_types
            ORDER BY is_direct DESC
        """

        if publisher not in (None, "", "null"):
            filtered_options_cte = "filtered_options AS (SELECT job_id, option FROM expanded_options WHERE option ->> 'publisher' = :publisher),"
            source_table = "filtered_options"
        else:
            filtered_options_cte = ""
            source_table = "expanded_options"

        query = text(
            base_query.format(
                where_clause=where_clause,
                filtered_options_cte=filtered_options_cte,
                source_table=source_table,
            )
        )

        result = db.execute(query, params)
        distribution = result.mappings().all()
        return distribution

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# CSV Export Endpoints


def get_job_platforms(db: Session) -> list[str]:
    """Get list of job platform names that should be excluded from company data"""
    try:
        query = text(
            """
            SELECT DISTINCT job_publisher
            FROM target.job_dashboard_base
            WHERE is_job_platform = true
            AND job_publisher IS NOT NULL
            AND job_publisher != ''
        """
        )

        result = db.execute(query)
        platforms = [row[0] for row in result]
        return platforms
    except Exception as e:
        print(f"ERROR getting job platforms: {str(e)}")
        return []


def build_where_clause_and_params(filters: CSVExportFilters):
    """Build WHERE clause and parameters from filters with comprehensive input validation"""
    try:
        conditions = []
        params = {}

        # Validate date inputs
        if filters.job_posted_at_date_from:
            validated_date_from = SecureQueryBuilder.validate_date_input(
                filters.job_posted_at_date_from, "job_posted_at_date_from"
            )
            conditions.append("jdb.job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if filters.job_posted_at_date_to:
            validated_date_to = SecureQueryBuilder.validate_date_input(
                filters.job_posted_at_date_to, "job_posted_at_date_to"
            )
            conditions.append("jdb.job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if filters.search_position_query:
            validated_position = SecureQueryBuilder.validate_text_input(
                filters.search_position_query, "search_position_query"
            )
            conditions.append("jdb.search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate array inputs with individual element validation
        if filters.employer_names:
            validated_employers = []
            for employer in filters.employer_names:
                validated_employer = SecureQueryBuilder.validate_text_input(
                    employer, "employer_name"
                )
                validated_employers.append(validated_employer)
            conditions.append("jdb.employer_name = ANY(:employer_names)")
            params["employer_names"] = validated_employers

        if filters.seniority_levels:
            validated_seniorities = []
            for seniority in filters.seniority_levels:
                validated_seniority = SecureQueryBuilder.validate_text_input(
                    seniority, "seniority"
                )
                validated_seniorities.append(validated_seniority)
            conditions.append("jdb.seniority = ANY(:seniority_levels)")
            params["seniority_levels"] = validated_seniorities

        if filters.employment_types:
            validated_employment_types = []
            for emp_type in filters.employment_types:
                validated_emp_type = SecureQueryBuilder.validate_text_input(
                    emp_type, "employment_type"
                )
                validated_employment_types.append(validated_emp_type)
            conditions.append("jdb.job_employment_type = ANY(:employment_types)")
            params["employment_types"] = validated_employment_types

        if filters.cities:
            validated_cities = []
            for city in filters.cities:
                validated_city = SecureQueryBuilder.validate_text_input(city, "city")
                validated_cities.append(validated_city)
            conditions.append("jdb.job_city = ANY(:cities)")
            params["cities"] = validated_cities

        if filters.states:
            validated_states = []
            for state in filters.states:
                validated_state = SecureQueryBuilder.validate_text_input(state, "state")
                validated_states.append(validated_state)
            conditions.append("jdb.job_state = ANY(:states)")
            params["states"] = validated_states

        # Validate boolean inputs
        if filters.job_is_remote is not None:
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                filters.job_is_remote, "job_is_remote"
            )
            conditions.append("jdb.job_is_remote = :job_is_remote")
            params["job_is_remote"] = validated_remote

        if filters.is_direct is not None:
            validated_direct = SecureQueryBuilder.validate_boolean_input(
                filters.is_direct, "is_direct"
            )
            conditions.append(
                """
                EXISTS (
                    SELECT 1 FROM jsonb_array_elements(jdb.apply_options::jsonb) AS ao
                    WHERE (ao ->> 'is_direct')::boolean = :is_direct
                )
            """
            )
            params["is_direct"] = validated_direct

        # Handle publishers and skills separately as they involve array operations
        if filters.publishers:
            validated_publishers = []
            for publisher in filters.publishers:
                validated_publisher = SecureQueryBuilder.validate_text_input(
                    publisher, "publisher"
                )
                validated_publishers.append(validated_publisher)
            conditions.append(
                """
                EXISTS (
                    SELECT 1 FROM jsonb_array_elements(jdb.apply_options::jsonb) AS ao
                    WHERE ao ->> 'publisher' = ANY(:publishers)
                )
            """
            )
            params["publishers"] = validated_publishers

        if filters.skills:
            validated_skills = []
            for skill in filters.skills:
                validated_skill = SecureQueryBuilder.validate_text_input(skill, "skill")
                validated_skills.append(validated_skill)
            conditions.append(
                """
                EXISTS (
                    SELECT 1 FROM jsonb_array_elements_text(jdb.extracted_skills::jsonb) AS skill
                    WHERE skill = ANY(:skills)
                )
            """
            )
            params["skills"] = validated_skills

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        return where_clause, params

    except ValueError as e:
        raise ValueError(f"Invalid filter input: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error building filter conditions: {str(e)}")


@app.post("/api/reports/count-export-records", response_model=ExportCountResponse)
async def count_export_records(
    request: CSVExportRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Count the number of records that would be exported with the given filters"""
    try:
        # Validate max_records parameter
        validated_max_records = SecureQueryBuilder.validate_integer_input(
            request.max_records, "max_records", 1, 50000
        )

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(request.filters)

        count_query = text(
            f"""
            SELECT COUNT(*) as total_count
            FROM target.job_dashboard_base jdb
            {where_clause}
        """
        )

        result = db.execute(count_query, params)
        count = result.scalar()

        return ExportCountResponse(count=count, max_allowed=validated_max_records)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/reports/export-csv")
async def export_csv(
    request: CSVExportRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    """Export job data as CSV with comprehensive filtering"""
    try:
        # Validate max records with secure input validation
        validated_max_records = SecureQueryBuilder.validate_integer_input(
            request.max_records, "max_records", 1, 50000
        )

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(request.filters)
        params["limit"] = validated_max_records

        # Build the main query to get all job data
        query = text(
            f"""
            SELECT 
                jdb.job_id,
                jdb.job_title,
                jdb.employer_name,
                jdb.job_posted_at_date,
                jdb.job_city,
                jdb.job_state,
                jdb.seniority,
                jdb.job_employment_type,
                jdb.job_is_remote,
                jdb.job_publisher,
                jdb.extracted_skills,
                jdb.apply_options,
                jdb.search_position_query,
                jdb.created_at,
                jdb.updated_at
            FROM target.job_dashboard_base jdb
            {where_clause}
            ORDER BY jdb.job_posted_at_date DESC
            LIMIT :limit
        """
        )

        result = db.execute(query, params)
        jobs = result.mappings().all()

        # Create CSV in memory with proper UTF-8 encoding for Brazilian Portuguese
        output = io.StringIO()
        writer = csv.writer(output)

        # Write CSV headers
        headers = [
            "job_id",
            "job_title",
            "employer_name",
            "job_posted_at_date",
            "job_city",
            "job_state",
            "seniority",
            "job_employment_type",
            "job_is_remote",
            "job_publisher",
            "extracted_skills",
            "apply_options",
            "search_position_query",
            "created_at",
            "updated_at",
        ]
        writer.writerow(headers)

        # Write data rows with proper string handling
        for job in jobs:
            row = [
                str(job.job_id or ""),
                str(job.job_title or ""),
                str(job.employer_name or ""),
                str(job.job_posted_at_date) if job.job_posted_at_date else "",
                str(job.job_city or ""),
                str(job.job_state or ""),
                str(job.seniority or ""),
                str(job.job_employment_type or ""),
                "Sim" if job.job_is_remote else "Não",  # Portuguese Yes/No
                str(job.job_publisher or ""),
                str(job.extracted_skills or ""),
                str(job.apply_options or ""),
                str(job.search_position_query or ""),
                job.created_at.isoformat() if job.created_at else "",
                job.updated_at.isoformat() if job.updated_at else "",
            ]
            writer.writerow(row)

        # Prepare response with UTF-8 BOM for proper encoding recognition
        output.seek(0)
        csv_content = output.getvalue()
        output.close()

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jobs_export_{timestamp}.csv"

        # Return as streaming response with UTF-8 BOM
        def generate():
            # UTF-8 BOM (Byte Order Mark) for proper encoding detection
            yield b"\xef\xbb\xbf"
            yield csv_content.encode("utf-8")

        return StreamingResponse(
            generate(),
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{filename}",
                "Content-Type": "text/csv; charset=utf-8",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exporting CSV: {str(e)}")


@app.get("/api/reports/preview-export", response_model=list[schemas.JobExportData])
async def preview_export(
    job_posted_at_date_from: Optional[str] = Query(None),
    job_posted_at_date_to: Optional[str] = Query(None),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    employer_names: Optional[str] = Query(
        None, description="Comma-separated list of employer names"
    ),
    publishers: Optional[str] = Query(
        None, description="Comma-separated list of publishers"
    ),
    seniority_levels: Optional[str] = Query(
        None, description="Comma-separated list of seniority levels"
    ),
    employment_types: Optional[str] = Query(
        None, description="Comma-separated list of employment types"
    ),
    cities: Optional[str] = Query(None, description="Comma-separated list of cities"),
    states: Optional[str] = Query(None, description="Comma-separated list of states"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    job_is_remote: Optional[bool] = Query(None),
    is_direct: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1, le=1000),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Preview the first N records that would be exported"""
    try:
        # Validate limit parameter
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 1000
        )

        # Parse and validate comma-separated parameters
        filters = CSVExportFilters(
            job_posted_at_date_from=job_posted_at_date_from,
            job_posted_at_date_to=job_posted_at_date_to,
            search_position_query=search_position_query,
            employer_names=employer_names.split(",") if employer_names else [],
            publishers=publishers.split(",") if publishers else [],
            seniority_levels=seniority_levels.split(",") if seniority_levels else [],
            employment_types=employment_types.split(",") if employment_types else [],
            cities=cities.split(",") if cities else [],
            states=states.split(",") if states else [],
            skills=skills.split(",") if skills else [],
            job_is_remote=job_is_remote,
            is_direct=is_direct,
        )

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(filters)
        params["limit"] = validated_limit

        # Use JOIN approach for job platform exclusion
        if job_platforms:
            # Create a CTE for job platforms to exclude
            platform_cte = """
            WITH job_platforms_to_exclude AS (
                SELECT DISTINCT job_publisher as platform_name
                FROM target.job_dashboard_base
                WHERE is_job_platform = true
                AND job_publisher IS NOT NULL
                AND job_publisher != ''
            )
            """

            query = text(
                f"""
            {platform_cte}
            SELECT 
                jdb.job_id,
                jdb.job_title,
                jdb.employer_name,
                jdb.job_posted_at_date,
                jdb.job_city,
                jdb.job_state,
                jdb.seniority,
                jdb.job_employment_type,
                jdb.job_is_remote,
                jdb.job_publisher,
                jdb.extracted_skills,
                jdb.apply_options,
                jdb.search_position_query,
                jdb.created_at,
                jdb.updated_at
            FROM target.job_dashboard_base jdb
            LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
            {where_clause}
            AND jpe.platform_name IS NULL
            ORDER BY jdb.job_posted_at_date DESC
            LIMIT :limit
            """
            )
        else:
            query = text(
                f"""
                SELECT 
                    jdb.job_id,
                    jdb.job_title,
                    jdb.employer_name,
                    jdb.job_posted_at_date,
                    jdb.job_city,
                    jdb.job_state,
                    jdb.seniority,
                    jdb.job_employment_type,
                    jdb.job_is_remote,
                    jdb.job_publisher,
                    jdb.extracted_skills,
                    jdb.apply_options,
                    jdb.search_position_query,
                    jdb.created_at,
                    jdb.updated_at
                FROM target.job_dashboard_base jdb
                {where_clause}
                ORDER BY jdb.job_posted_at_date DESC
                LIMIT :limit
            """
            )

        result = db.execute(query, params)
        jobs = result.mappings().all()
        return jobs

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# Public endpoints for data preview (no authentication required)
@app.get("/api/public/preview-export", response_model=list[schemas.JobExportData])
async def public_preview_export(
    job_posted_at_date_from: Optional[str] = Query(None),
    job_posted_at_date_to: Optional[str] = Query(None),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    employer_names: Optional[str] = Query(
        None, description="Comma-separated list of employer names"
    ),
    publishers: Optional[str] = Query(
        None, description="Comma-separated list of publishers"
    ),
    seniority_levels: Optional[str] = Query(
        None, description="Comma-separated list of seniority levels"
    ),
    employment_types: Optional[str] = Query(
        None, description="Comma-separated list of employment types"
    ),
    cities: Optional[str] = Query(None, description="Comma-separated list of cities"),
    states: Optional[str] = Query(None, description="Comma-separated list of states"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    job_is_remote: Optional[bool] = Query(None),
    is_direct: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Public endpoint for previewing export data (no authentication required)
    Used for the home page data preview section
    """
    try:
        # Validate limit parameter
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 1000
        )

        # Parse and validate comma-separated parameters
        filters = CSVExportFilters(
            job_posted_at_date_from=job_posted_at_date_from,
            job_posted_at_date_to=job_posted_at_date_to,
            search_position_query=search_position_query,
            employer_names=employer_names.split(",") if employer_names else [],
            publishers=publishers.split(",") if publishers else [],
            seniority_levels=seniority_levels.split(",") if seniority_levels else [],
            employment_types=employment_types.split(",") if employment_types else [],
            cities=cities.split(",") if cities else [],
            states=states.split(",") if states else [],
            skills=skills.split(",") if skills else [],
            job_is_remote=job_is_remote,
            is_direct=is_direct,
        )

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(filters)
        params["limit"] = validated_limit

        # Use JOIN approach for job platform exclusion
        if job_platforms:
            # Create a CTE for job platforms to exclude
            platform_cte = """
            WITH job_platforms_to_exclude AS (
                SELECT DISTINCT job_publisher as platform_name
                FROM target.job_dashboard_base
                WHERE is_job_platform = true
                AND job_publisher IS NOT NULL
                AND job_publisher != ''
            )
            """

            query = text(
                f"""
            {platform_cte}
            SELECT 
                jdb.job_id,
                jdb.job_title,
                jdb.employer_name,
                jdb.job_posted_at_date,
                jdb.job_city,
                jdb.job_state,
                jdb.seniority,
                jdb.job_employment_type,
                jdb.job_is_remote,
                jdb.job_publisher,
                jdb.extracted_skills,
                jdb.apply_options,
                jdb.search_position_query,
                jdb.created_at,
                jdb.updated_at
            FROM target.job_dashboard_base jdb
            LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
            {where_clause}
            AND jpe.platform_name IS NULL
            ORDER BY jdb.job_posted_at_date DESC
            LIMIT :limit
            """
            )
        else:
            query = text(
                f"""
                SELECT 
                    jdb.job_id,
                    jdb.job_title,
                    jdb.employer_name,
                    jdb.job_posted_at_date,
                    jdb.job_city,
                    jdb.job_state,
                    jdb.seniority,
                    jdb.job_employment_type,
                    jdb.job_is_remote,
                    jdb.job_publisher,
                    jdb.extracted_skills,
                    jdb.apply_options,
                    jdb.search_position_query,
                    jdb.created_at,
                    jdb.updated_at
                FROM target.job_dashboard_base jdb
                {where_clause}
                ORDER BY jdb.job_posted_at_date DESC
                LIMIT :limit
            """
            )

        result = db.execute(query, params)
        jobs = result.mappings().all()
        return jobs

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/public/count-export-records", response_model=ExportCountResponse)
async def public_count_export_records(
    request: CSVExportRequest, db: Session = Depends(get_db)
):
    """
    Public endpoint for counting export records (no authentication required)
    Used for the home page data preview section
    """
    try:
        # Build where clause and params
        where_clause, params = build_where_clause_and_params(request.filters)

        # Count total records
        count_query = text(
            f"""
            SELECT COUNT(*) as total_records
            FROM target.job_dashboard_base jdb
            {where_clause}
        """
        )

        result = db.execute(count_query, params)
        total_records = result.scalar()

        return ExportCountResponse(count=total_records, max_allowed=request.max_records)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting records: {str(e)}")


@app.get("/api/public/available-positions", response_model=list[str])
async def public_get_available_positions(db: Session = Depends(get_db)):
    """
    Public endpoint for getting available positions (no authentication required)
    Used for the home page data preview section
    """
    try:
        # Use parameterized query (no user input, so safe)
        query = text(
            """
            SELECT DISTINCT search_position_query
            FROM target.job_dashboard_base
            WHERE search_position_query IS NOT NULL AND search_position_query != ''
            ORDER BY search_position_query
            LIMIT 50
        """
        )

        result = db.execute(query)
        positions = [row[0] for row in result]
        return positions

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching positions: {str(e)}"
        )


@app.get("/api/reports/available-locations", response_model=dict)
async def get_available_locations(db: Session = Depends(get_db)):
    """Get available cities and states for filtering"""
    try:
        query = text(
            """
            SELECT DISTINCT 
                job_city,
                job_state
            FROM target.job_dashboard_base
            WHERE job_city IS NOT NULL AND job_state IS NOT NULL
            ORDER BY job_state, job_city
        """
        )

        result = db.execute(query)
        locations = result.mappings().all()

        cities = sorted(list(set([loc.job_city for loc in locations if loc.job_city])))
        states = sorted(
            list(set([loc.job_state for loc in locations if loc.job_state]))
        )

        return {"cities": cities, "states": states}

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error fetching locations: {str(e)}"
        )


@app.get("/api/reports/available-employment-types", response_model=list[str])
async def get_available_employment_types(db: Session = Depends(get_db)):
    """Get available employment types for filtering"""
    try:
        query = text(
            """
            SELECT DISTINCT job_employment_type
            FROM target.job_dashboard_base
            WHERE job_employment_type IS NOT NULL
            ORDER BY job_employment_type
        """
        )

        result = db.execute(query)
        types = [row[0] for row in result.fetchall()]
        return types

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error fetching employment types: {str(e)}"
        )


@app.get("/api/dashboard/job-locations-geo")
def get_job_locations_geo(
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    job_city: Optional[str] = Query(None, description="Filter by city"),
    job_state: Optional[str] = Query(None, description="Filter by state"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    limit: int = Query(500, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Get geographic job location data with comprehensive filtering"""
    try:
        # Validate limit parameter
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 1000
        )

        filters = []
        params = {"limit": validated_limit}

        # Validate and add date filters
        if job_posted_at_date_from:
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to:
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate and add text filters
        if employer_name:
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority:
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if job_city:
            validated_city = SecureQueryBuilder.validate_text_input(
                job_city, "job_city"
            )
            filters.append("job_city = :job_city")
            params["job_city"] = validated_city

        if job_state:
            validated_state = SecureQueryBuilder.validate_text_input(
                job_state, "job_state"
            )
            filters.append("job_state = :job_state")
            params["job_state"] = validated_state

        # Validate and add search position query with secure ILIKE
        if search_position_query:
            validated_search = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query ILIKE :search_position_query")
            params["search_position_query"] = f"%{validated_search}%"

        # Validate and add boolean filter
        if job_is_remote is not None:
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            filters.append("job_is_remote = :job_is_remote")
            params["job_is_remote"] = validated_remote

        # Always filter out null or placeholder values (static filters)
        location_filters = [
            "job_city IS NOT NULL",
            "job_city != 'Brasil (N/A)'",
            "job_city != ''",
            "job_state IS NOT NULL",
            "job_state != 'Brasil (N/A)'",
            "job_state != ''",
        ]

        # Combine all filters
        all_filters = filters + location_filters
        where_clause = f"WHERE {' AND '.join(all_filters)}" if all_filters else ""

        query = text(
            f"""
            SELECT 
                job_city,
                job_state,
                COUNT(*) as job_count
            FROM target.job_dashboard_base
            {where_clause}
            GROUP BY job_city, job_state
            ORDER BY job_count DESC
            LIMIT :limit
        """
        )

        result = db.execute(query, params)
        locations = result.mappings().all()

        return locations

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")





# Skills filtering endpoint
@app.get("/api/skills/jobs", response_model=list[schemas.JobExportData])
async def get_jobs_by_skills(
    skills: str = Query(..., description="Comma-separated list of skills to filter by"),
    job_posted_at_date_from: Optional[str] = Query(None),
    job_posted_at_date_to: Optional[str] = Query(None),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    employer_names: Optional[str] = Query(
        None, description="Comma-separated list of employer names"
    ),
    publishers: Optional[str] = Query(
        None, description="Comma-separated list of publishers"
    ),
    seniority_levels: Optional[str] = Query(
        None, description="Comma-separated list of seniority levels"
    ),
    employment_types: Optional[str] = Query(
        None, description="Comma-separated list of employment types"
    ),
    cities: Optional[str] = Query(None, description="Comma-separated list of cities"),
    states: Optional[str] = Query(None, description="Comma-separated list of states"),
    job_is_remote: Optional[bool] = Query(None),
    is_direct: Optional[bool] = Query(None),
    limit: int = Query(10000, ge=1, le=50000),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get jobs filtered by specific skills with optimized query for skills filtering.
    This endpoint uses a specialized query that efficiently searches for skills in the extracted_skills field.
    """
    try:
        # Validate limit parameter
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 50000
        )

        # Parse and validate comma-separated parameters
        filters = CSVExportFilters(
            job_posted_at_date_from=job_posted_at_date_from,
            job_posted_at_date_to=job_posted_at_date_to,
            search_position_query=search_position_query,
            employer_names=employer_names.split(",") if employer_names else [],
            publishers=publishers.split(",") if publishers else [],
            seniority_levels=seniority_levels.split(",") if seniority_levels else [],
            employment_types=employment_types.split(",") if employment_types else [],
            cities=cities.split(",") if cities else [],
            states=states.split(",") if states else [],
            skills=skills.split(",") if skills else [],
            job_is_remote=job_is_remote,
            is_direct=is_direct,
        )

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(filters)
        params["limit"] = validated_limit

        # Simplified skills filtering query
        query = text(
            f"""
            SELECT 
                jdb.job_id,
                jdb.job_title,
                jdb.employer_name,
                jdb.job_posted_at_date,
                jdb.job_city,
                jdb.job_state,
                jdb.seniority,
                jdb.job_employment_type,
                jdb.job_is_remote,
                jdb.job_publisher,
                jdb.extracted_skills,
                jdb.apply_options,
                jdb.search_position_query,
                jdb.created_at,
                jdb.updated_at
            FROM target.job_dashboard_base jdb
            {where_clause}
            ORDER BY jdb.job_posted_at_date DESC
            LIMIT :limit
        """
        )

        result = db.execute(query, params)
        jobs = result.mappings().all()
        return jobs

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# Contact form endpoint
# Cache management endpoints (for development/monitoring)
@app.get("/api/cache/status")
async def get_cache_status():
    """Get cache status and statistics"""
    return {
        "cache_size": query_cache.size(),
        "cache_enabled": True,
        "default_ttl": query_cache.default_ttl,
    }


@app.post("/api/cache/clear")
async def clear_cache():
    """Clear all cached data"""
    query_cache.clear()
    return {"message": "Cache cleared successfully"}


@app.post("/api/contact", response_model=ContactResponse)
async def send_contact_email(contact_data: ContactForm):
    """
    Send contact form email
    """
    try:
        # Import here to avoid circular imports
        from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
        import os

        # Email configuration
        conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),
            MAIL_FROM=os.getenv(
                "MAIL_FROM", "your-email@gmail.com"
            ),  # Should match MAIL_USERNAME for Gmail
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        # Create email message
        html_content = f"""
        <h2>Nova mensagem de contato - HireMetrics</h2>
        <p><strong>Nome:</strong> {contact_data.name}</p>
        <p><strong>E-mail:</strong> {contact_data.email}</p>
        <p><strong>Empresa:</strong> {contact_data.company or 'Não informado'}</p>
        <p><strong>Assunto:</strong> {contact_data.subject}</p>
        <p><strong>Mensagem:</strong></p>
        <p>{contact_data.message.replace(chr(10), '<br>')}</p>
        <hr>
        <p><small>Enviado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</small></p>
        """

        message = MessageSchema(
            subject=f"Contato HireMetrics: {contact_data.subject}",
            recipients=["hiremetrics.contato@gmail.com"],
            body=html_content,
            subtype="html",
        )

        # Send email
        fm = FastMail(conf)
        await fm.send_message(message)

        return ContactResponse(
            success=True,
            message="Mensagem enviada com sucesso! Entraremos em contato em breve.",
        )

    except Exception as e:
        print(f"Error sending contact email: {e}")
        import traceback

        traceback.print_exc()

        # Provide more specific error messages
        error_message = "Erro ao enviar mensagem. Tente novamente ou entre em contato diretamente por e-mail."

        if "Authentication" in str(e):
            error_message = (
                "Erro de autenticação de e-mail. Verifique as credenciais configuradas."
            )
        elif "timeout" in str(e).lower():
            error_message = (
                "Timeout na conexão de e-mail. Verifique a configuração SMTP."
            )
        elif "connection" in str(e).lower():
            error_message = "Erro de conexão com servidor de e-mail. Verifique a configuração de rede."

        return ContactResponse(success=False, message=error_message)
