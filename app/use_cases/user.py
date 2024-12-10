"""User Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import User
from app.repositories.user import UserRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


# TBC Update function
class UserUseCase:
    """User Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db."""
        self.db = db
        self.user_repository = UserRepository(User)

    def get_users(self) -> Union[Page[schemas.UserOut], JSONResponse]:
        """Get all users record."""
        try:
            users = self.user_repository.get_all(self.db)

        except DatabaseException as e:
            logger.error(f"Database error occurred while fetching users: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(users)

    def get_user(self, _id: int) -> Union[schemas.UserOut, JSONResponse]:
        """Get user record."""
        try:
            user = self.user_repository.get(self.db, _id)

            return schemas.UserOut.model_validate(user)

        except APIException as e:
            logger.error(f"Database error occurred while fetching user: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def create_user(
        self,
        *,
        obj_in: schemas.UserIn,
    ) -> Union[schemas.UserOut, JSONResponse]:
        """Create user record."""
        try:
            user = self.user_repository.create_user_with_password(
                db=self.db, obj_in=obj_in
            )
            return schemas.UserOut.model_validate(user)

        except DatabaseException as e:
            logger.error(f"Database error occurred while creating user: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_user(self, _id: int) -> Union[schemas.UserOut, JSONResponse]:
        """Delete user record."""
        try:
            user_update = self.user_repository.delete(db=self.db, _id=_id)

            return schemas.UserOut.model_validate(user_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while deleting user: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
