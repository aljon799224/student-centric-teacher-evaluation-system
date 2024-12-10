"""User Repository."""

from http import HTTPStatus
from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserIn
from exceptions.exceptions import DatabaseException


class UserRepository(BaseRepository[User, UserIn, UserIn]):
    """User Repository Class."""

    @staticmethod
    def get_by_username(db: Session, *, username: str) -> Optional[User]:
        """Get by username."""
        return db.query(User).filter(User.username == username).first()

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
