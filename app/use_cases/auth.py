"""Authentication Use Case."""

from http import HTTPStatus
from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.core.security import create_access_token
from app.models import User
from app.repositories.user import UserRepository


class AuthenticationUseCase:
    """Authentication Use Case Class."""

    def __init__(self, db):
        """Initialize with db and User Repository."""
        self.db = db
        self.user_repository = UserRepository(User)

    def login_access_token(
        self, form_data: OAuth2PasswordRequestForm = Depends()
    ) -> Union[JSONResponse, dict]:
        """OAuth2 compatible token login, get an access token for future requests."""
        user = self.user_repository.authenticate(
            self.db, username=form_data.username, password=form_data.password
        )
        if not user:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={"message": "Incorrect username or password"},
            )

        access_token = create_access_token(
            data={
                "subject": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "email": user.email,
                "last_name": user.last_name,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
