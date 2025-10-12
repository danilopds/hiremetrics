"""Token service for JWT operations"""

from datetime import timedelta
from typing import Optional

from .. import models
from ..utils.auth_utils import create_access_token


def create_user_token(user: models.User, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token for user"""

    data = {
        "sub": user.email,
        "auth_provider": getattr(user, "auth_provider", "email"),  # Handle OAuth users
    }
    return create_access_token(data, expires_delta)
