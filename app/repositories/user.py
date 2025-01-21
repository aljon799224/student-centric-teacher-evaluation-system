"""User Repository."""

from http import HTTPStatus
from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.core.security import (
    get_password_hash,
    verify_password,
    verify_password_reset_token,
)
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserIn, UserUpdate
from exceptions.exceptions import DatabaseException


class UserRepository(BaseRepository[User, UserIn, UserUpdate]):
    """User Repository Class."""

    @staticmethod
    def get_by_username(db: Session, *, username: str) -> Optional[User]:
        """Get by username."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[User]:
        """Get by email."""
        return db.query(User).filter(User.email == email).first()

    def create_user_with_password(
        self, db: Session, *, obj_in: UserIn
    ) -> Optional[User]:
        """Create user with password."""
        try:
            obj_in_data = jsonable_encoder(obj_in)

            obj_in_data.update({"hashed_password": get_password_hash(obj_in.password)})
            del obj_in_data["password"]
            db_obj = self.model(**obj_in_data)  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        except exc.IntegrityError as e:
            error = e.orig.args

            raise DatabaseException(
                status_code=HTTPStatus.CONFLICT, detail=error[0]
            ) from e

        except Exception as e:
            raise DatabaseException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            ) from e

        return db_obj

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        """Authenticate."""
        user = self.get_by_username(db, username=username)  # noqa
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def reset_password(
        self, db: Session, new_password: str, token: str
    ) -> Union[dict[str, str], JSONResponse]:
        """Reset Password."""
        email = verify_password_reset_token(token)
        if not email:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"message": "Invalid token"},
            )
        user = self.get_by_email(db, email=email)

        if not user:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND, content={"message": "User no found"}
            )

        hash_password = get_password_hash(new_password)
        user.hashed_password = hash_password
        db.add(user)
        db.commit()
        return {"message": "Password updated successfully"}
