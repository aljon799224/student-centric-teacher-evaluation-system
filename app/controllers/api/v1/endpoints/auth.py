"""Auth Endpoint."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

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
