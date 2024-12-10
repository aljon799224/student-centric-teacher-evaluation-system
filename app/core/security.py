"""Security."""

import logging
from typing import Union

import bcrypt

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import schemas
from app.core.config import settings
from app.db.session import get_db
from app.models import User

logger = logging.getLogger(__name__)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(data: dict):
    """Create access token."""
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    expire_timestamp = int(expire.timestamp())  # Convert to Unix timestamp
    to_encode.update({"exp": expire_timestamp})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Union[User, None]:  # pragma: no cover
    """Get current user."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)

        # use lazy import to avoid circular import error
        from app.repositories.user import UserRepository

        user_repo = UserRepository(User)
        user = user_repo.get(db, token_data.subject)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except (JWTError, ValidationError):
        return None

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return None


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user."""
    return current_user
