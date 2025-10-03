from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import models, schemas
from .utils.auth import get_password_hash, verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)

    db_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        marketing_emails=True,  # Default to receiving marketing emails
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_oauth_user(db: Session, user_data: dict):
    """Create user from OAuth provider data"""
    now = datetime.now(timezone.utc)

    db_user = models.User(
        email=user_data["email"],
        password_hash="",  # OAuth users don't have passwords
        first_name=user_data.get("first_name", ""),
        last_name=user_data.get("last_name", ""),
        auth_provider=user_data.get("auth_provider", "google"),
        google_id=user_data.get("google_id"),
        email_verified=True,  # OAuth users are pre-verified
        last_login=now,  # Set initial login time
        marketing_emails=True,  # Default to receiving marketing emails
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    user.last_login = datetime.utcnow()
    db.commit()
    return user


def change_user_password(
    db: Session, user_id: int, current_password: str, new_password: str
):
    """Change user password after verifying current password"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return False

    # Verify current password
    if not pwd_context.verify(current_password, user.password_hash):
        return False

    # Hash and update new password
    hashed_password = pwd_context.hash(new_password)
    user.password_hash = hashed_password
    db.commit()
    db.refresh(user)
    return True


# Email verification functions
def create_user_with_verification(db: Session, user: schemas.UserCreate):
    """Create user with email verification token"""
    import secrets

    hashed_password = get_password_hash(user.password)
    now = datetime.now(timezone.utc)

    # Generate verification token
    verification_token = secrets.token_urlsafe(32)
    verification_expires = now + timedelta(hours=24)  # Token expires in 24 hours

    db_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        company=user.company,
        job_title=user.job_title,
        industry=user.industry,
        company_size=user.company_size,
        role_in_company=user.role_in_company,
        email_verified=False,
        email_verification_token=verification_token,
        email_verification_expires=verification_expires,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_verification_token(db: Session, token: str):
    """Get user by email verification token"""
    return (
        db.query(models.User)
        .filter(
            models.User.email_verification_token == token,
            models.User.email_verification_expires > datetime.now(timezone.utc),
        )
        .first()
    )


def verify_user_email(db: Session, token: str):
    """Verify user email"""
    user = get_user_by_verification_token(db, token)
    if not user:
        return False, "Token inválido ou expirado"

    user.email_verified = True
    user.email_verification_token = None
    user.email_verification_expires = None

    db.commit()
    db.refresh(user)
    return True, "Email verificado com sucesso!"


def resend_verification_email(db: Session, email: str):
    """Resend verification email"""
    import secrets

    user = get_user_by_email(db, email)
    if not user:
        return False, "Email não encontrado"

    if user.email_verified:
        return False, "Email já foi verificado"

    # Generate new verification token
    verification_token = secrets.token_urlsafe(32)
    verification_expires = datetime.now(timezone.utc) + timedelta(hours=24)

    user.email_verification_token = verification_token
    user.email_verification_expires = verification_expires

    db.commit()
    db.refresh(user)
    return True, "Novo email de verificação enviado"


def request_password_reset(db: Session, email: str):
    """Request password reset for user"""
    import secrets

    user = get_user_by_email(db, email)
    if not user:
        return False, "Email não encontrado"

    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    reset_expires = datetime.now(timezone.utc) + timedelta(
        hours=1
    )  # Token expires in 1 hour

    user.password_reset_token = reset_token
    user.password_reset_expires = reset_expires

    db.commit()
    db.refresh(user)
    return True, "Email de redefinição de senha enviado"


def get_user_by_reset_token(db: Session, token: str):
    """Get user by password reset token"""
    return (
        db.query(models.User)
        .filter(
            models.User.password_reset_token == token,
            models.User.password_reset_expires > datetime.now(timezone.utc),
        )
        .first()
    )


def reset_user_password(db: Session, token: str, new_password: str):
    """Reset user password using token"""
    user = get_user_by_reset_token(db, token)
    if not user:
        return False, "Token inválido ou expirado"

    # Hash new password
    hashed_password = get_password_hash(new_password)

    # Update password and clear reset token
    user.password_hash = hashed_password
    user.password_reset_token = None
    user.password_reset_expires = None

    db.commit()
    db.refresh(user)
    return True, "Senha alterada com sucesso"


def validate_reset_token(db: Session, token: str):
    """Validate password reset token"""
    user = get_user_by_reset_token(db, token)
    if not user:
        return False, "Token inválido ou expirado"
    return True, "Token válido"
