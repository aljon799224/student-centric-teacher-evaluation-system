"""Auth Endpoint."""

from typing import Union

from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.db.session import get_db
from app.use_cases.auth import AuthenticationUseCase

auth_router = APIRouter()


@auth_router.post("/auth/login/token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """OAuth2 compatible token login, get an access token for future requests."""
    auth_uc = AuthenticationUseCase(db=db)
    response = auth_uc.login_access_token(form_data=form_data)
    return response


@auth_router.post("/reset-password", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db),
) -> Union[JSONResponse, dict]:
    """Reset password."""
    auth_uc = AuthenticationUseCase(db=db)
    response = auth_uc.reset_password(new_password=new_password, token=token)
    return response
