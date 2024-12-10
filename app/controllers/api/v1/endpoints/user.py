"""User Endpoint."""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.user import UserUseCase

user_router = APIRouter()


@user_router.get("/user", response_model=Page[schemas.UserOut])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all users."""
    user_uc = UserUseCase(db=db)

    users = user_uc.get_users()

    return users


@user_router.get("/user/{_id}", response_model=schemas.UserOut)
def get_user(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get user by ID."""
    user_uc = UserUseCase(db=db)

    user = user_uc.get_user(_id=_id)

    return user


@user_router.post("/user", response_model=schemas.UserOut)
def create(obj_in: schemas.UserIn, db: Session = Depends(get_db)):
    """Create user."""
    user_uc = UserUseCase(db=db)

    user = user_uc.create_user(obj_in=obj_in)

    return user


@user_router.delete("/user/{_id}", response_model=schemas.UserOut)
def delete(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Delete user by ID."""
    user_uc = UserUseCase(db=db)

    user = user_uc.delete_user(_id=_id)

    return user
