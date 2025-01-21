"""User Schema."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class UserRoleEnum(str, Enum):
    """User Roles."""

    admin = "admin"
    teacher = "teacher"
    student = "student"


class UserBase(BaseModel):
    """User Base Class."""

    model_config = ConfigDict(from_attributes=True)

    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    disabled: bool = False
    role: UserRoleEnum = UserRoleEnum.admin
    temp_pwd: bool = False
    admin_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserUpdate(UserBase):
    """User Update Class."""

    pass


class UserIn(UserBase):
    """User In Class."""

    password: str


class UserOut(UserBase):
    """User Out Class."""

    id: int
