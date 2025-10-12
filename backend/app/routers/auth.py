"""Authentication endpoints"""

from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..config import settings
from ..database import get_db
from ..services.email_service import send_password_reset_email, send_verification_email
from ..services.token_service import create_user_token
from ..utils.auth_utils import get_current_user

router = APIRouter()


@router.post("/register", response_model=schemas.RegistrationResponse)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
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


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login endpoint"""
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


@router.post("/verify-email", response_model=schemas.EmailVerificationResponse)
async def verify_email(request: schemas.EmailVerificationRequest, db: Session = Depends(get_db)):
    """Verify user email with token"""
    success, message = crud.verify_user_email(db, request.token)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return schemas.EmailVerificationResponse(success=True, message=message)


@router.post("/resend-verification", response_model=schemas.ResendVerificationResponse)
async def resend_verification(
    request: schemas.ResendVerificationRequest, db: Session = Depends(get_db)
):
    """Resend verification email"""
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


@router.post("/forgot-password", response_model=schemas.ForgotPasswordResponse)
async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request password reset"""
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


@router.post("/reset-password", response_model=schemas.ResetPasswordResponse)
async def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset user password with token"""
    success, message = crud.reset_user_password(db, request.token, request.new_password)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return schemas.ResetPasswordResponse(success=True, message=message)


@router.post("/validate-reset-token", response_model=schemas.ValidateResetTokenResponse)
async def validate_reset_token(
    request: schemas.ValidateResetTokenRequest, db: Session = Depends(get_db)
):
    """Validate password reset token"""
    success, message = crud.validate_reset_token(db, request.token)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return schemas.ValidateResetTokenResponse(success=True, message=message)


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/google/login")
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


@router.get("/google/callback")
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
        return RedirectResponse(url=f"{frontend_url}/auth/google-callback?error={error}")

    # Check if code is provided
    if not code:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        return RedirectResponse(url=f"{frontend_url}/auth/google-callback?error=missing_code")

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
        return RedirectResponse(url=f"{frontend_url}/auth/google-callback?token={access_token}")

    except requests.RequestException as e:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        error_msg = f"google_oauth_error: {str(e)}"
        return RedirectResponse(url=f"{frontend_url}/auth/google-callback?error={error_msg}")
    except Exception as e:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        error_msg = f"authentication_error: {str(e)}"
        return RedirectResponse(url=f"{frontend_url}/auth/google-callback?error={error_msg}")


@router.post("/change-password", response_model=schemas.PasswordChangeResponse)
async def change_password(
    password_data: schemas.PasswordChange,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change user password"""
    success = crud.change_user_password(
        db,
        str(current_user.id),
        password_data.current_password,
        password_data.new_password,
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha atual incorreta")

    return schemas.PasswordChangeResponse(message="Senha alterada com sucesso!")


@router.put("/preferences", response_model=schemas.UserPreferencesUpdate)
async def update_user_preferences(
    preferences: schemas.UserPreferencesUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user preferences"""
    success = crud.update_user_preferences(db, str(current_user.id), preferences.dict())

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar preferências",
        )

    return preferences
