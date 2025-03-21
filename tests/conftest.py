"""Conftest."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app import schemas
from app.models import User, Evaluation
from app.schemas.user import UserRoleEnum


@pytest.fixture()
def mock_session():
    """Create mock database session."""
    return MagicMock(spec=Session)


################################################ Auth


@pytest.fixture()
def login_access_token_out():
    """Fixture that returns response for the login access token."""
    return {
        "access_token": "access_token",
        "token_type": "bearer",
        "name": "John Doe",
        "user_id": 1,
        "temp_pwd": True,
        "role": "admin",
    }


@pytest.fixture()
def form_data_in_for_login_access_token():
    """Form data for login access token."""
    return {
        "username": "username",
        "password": "password",
    }


################################################ Item


@pytest.fixture()
def item_db_in():
    """Fixture that returns an ItemIn schema for creating/updating an item."""
    return schemas.ItemIn(name="New Item")


@pytest.fixture()
def item_db_out():
    """Fixture that returns an ItemOut schema."""
    return schemas.ItemOut(id=1, name="Item 1")


@pytest.fixture()
def item_out():
    """Fixture that returns an item in dictionary."""
    return {
        "id": 1,
        "name": "Item 1",
    }


@pytest.fixture()
def items_out():
    """Fixture that returns a paginated list of items in dictionary."""
    return {
        "items": [
            {
                "id": 1,
                "name": "Item 1",
            },
            {
                "id": 2,
                "name": "Item 2",
            },
        ],
        "total": 2,
        "page": 1,
        "size": 10,
        "pages": None,
    }


################################################ User


@pytest.fixture()
def user_model_out():
    """Fixture that returns a pre-configured User model instance."""
    mock_data = User()
    mock_data.id = 1
    mock_data.username = "User 1"
    mock_data.email = "user@yahoo.com"
    mock_data.first_name = "John"
    mock_data.middle_name = "Doe"
    mock_data.last_name = "Doe"
    mock_data.disabled = True
    mock_data.role = "admin"
    mock_data.temp_pwd = False
    mock_data.created_at = "2024-12-10T09:17:55.330000"
    mock_data.updated_at = "2024-12-10T09:17:55.330000"

    return mock_data


@pytest.fixture()
def user_db_in():
    """Fixture that returns a UserIn schema for creating an item."""
    # Manually convert datetime fields to ISO format

    return schemas.UserIn(
        username="User 1",
        email="user@yahoo.com",
        first_name="John",
        middle_name="Doe",
        last_name="Doe",
        disabled=True,
        password="password",
        role=UserRoleEnum.admin.value,
        temp_pwd=False,
        created_at=datetime(2024, 12, 10, 9, 17, 55, 330000),
        updated_at=datetime(2024, 12, 10, 9, 17, 55, 330000),
    )


@pytest.fixture()
def user_db_update():
    """Fixture that returns a UserUpdate schema for updating an item."""
    # Manually convert datetime fields to ISO format

    return schemas.UserUpdate(
        username="User 1 Update",
        email="user_update@yahoo.com",
        first_name="John Update",
        middle_name="Doe Update",
        last_name="Doe Update",
    )


@pytest.fixture()
def user_db_out():
    """Fixture that returns a UserOut schema."""
    return schemas.UserOut(
        id=1,
        username="User 1",
        email="user@yahoo.com",
        first_name="John",
        middle_name="Doe",
        last_name="Doe",
        disabled=True,
        role=UserRoleEnum.admin.value,
        temp_pwd=False,
        created_at="2024-12-10T09:17:55.330000",
        updated_at="2024-12-10T09:17:55.330000",
    )


@pytest.fixture()
def user_out():
    """Fixture that returns a user in dictionary."""
    return {
        "id": 1,
        "username": "User 1",
        "email": "user@yahoo.com",
        "first_name": "John",
        "middle_name": "Doe",
        "last_name": "Doe",
        "disabled": True,
        "created_at": "2024-12-10T09:17:55.330000",
        "role": "admin",
        "temp_pwd": False,
        "updated_at": "2024-12-10T09:17:55.330000",
        "admin_id": None,
    }


@pytest.fixture()
def users_out():
    """Fixture that returns a paginated list of users in dictionary."""
    return {
        "items": [
            {
                "id": 1,

            },
            {
                "id": 2,

            },
        ],
        "total": 2,
        "page": 1,
        "size": 10,
        "pages": None,
    }


################################################ Evaluation


@pytest.fixture()
def evaluation_model_out():
    """Fixture that returns a pre-configured Evaluation model instance."""
    mock_data = Evaluation()
    mock_data.id = 1
    mock_data.title = "evaluation 1"
    mock_data.teacher_id = 1
    mock_data.admin_id = 1
    mock_data.is_submitted = False
    mock_data.created_at = "2024-12-10T09:17:55.330000"
    mock_data.updated_at = "2024-12-10T09:17:55.330000"

    return mock_data


@pytest.fixture()
def evaluation_db_in():
    """Fixture that returns a EvaluationIn schema for creating an evaluation."""
    # Manually convert datetime fields to ISO format

    return schemas.EvaluationIn(
        title="evaluation 1",
        teacher_id=1,
        admin_id=1,
        is_submitted=False,
        created_at=datetime(2024, 12, 10, 9, 17, 55, 330000),
        updated_at=datetime(2024, 12, 10, 9, 17, 55, 330000),
    )


@pytest.fixture()
def evaluation_db_update():
    """Fixture that returns a EvaluationUpdate schema for updating an evaluation."""
    # Manually convert datetime fields to ISO format

    return schemas.EvaluationUpdate(
        title="evaluation 1 Update",
        teacher_id=2,
        is_submitted=False,
    )


@pytest.fixture()
def evaluation_db_out():
    """Fixture that returns a EvaluationOut schema."""
    return schemas.EvaluationOut(
        id=1,
        title="evaluation 1",
        teacher_id=1,
        is_submitted=False,
        admin_id=1,
        created_at="2024-12-10T09:17:55.330000",
        updated_at="2024-12-10T09:17:55.330000",
    )


@pytest.fixture()
def evaluation_detailed_db_out():
    """Fixture that returns a EvaluationOut schema."""
    return schemas.EvaluationDetailedOut(
        id=1,
        title="evaluation 1",
        teacher_id=1,
        teacher_name="John Doe Doe",
        is_submitted=False,
        admin_id=1,
        created_at="2024-12-10T09:17:55.330000",
        updated_at="2024-12-10T09:17:55.330000",
    )


@pytest.fixture()
def evaluation_out():
    """Fixture that returns an evaluation in dictionary."""
    return {
        "id": 1,
        "title": "evaluation 1",
        "teacher_id": 1,
        "admin_id": 1,
        "is_submitted": False,
        "created_at": "2024-12-10T09:17:55.330000",
        "updated_at": "2024-12-10T09:17:55.330000",
    }


@pytest.fixture()
def evaluation_detailed_out():
    """Fixture that returns a detailed evaluation in dictionary."""
    return {
        "id": 1,
        "title": "evaluation 1",
        "teacher_id": 1,
        "teacher_name": "John Doe Doe",
        "admin_id": 1,
        "is_submitted": False,
        "created_at": "2024-12-10T09:17:55.330000",
        "updated_at": "2024-12-10T09:17:55.330000",
    }


@pytest.fixture()
def evaluations_out():
    """Fixture that returns a paginated list of evaluations in dictionary."""
    return {
        "items": [
            {
                "id": 1,
                "title": "evaluation 1",
                "teacher_id": 1,
                "teacher_name": "John Doe Doe",
                "admin_id": 1,
                "is_submitted": False,
                "created_at": "2024-12-10T09:17:55.330000",
                "updated_at": "2024-12-10T09:17:55.330000",
            },
            {
                "id": 2,
                "title": "evaluation 2",
                "teacher_id": 1,
                "teacher_name": "John Doe Doe",
                "admin_id": 1,
                "is_submitted": False,
                "created_at": "2024-12-10T09:17:55.330000",
                "updated_at": "2024-12-10T09:17:55.330000",
            },
        ],
        "total": 2,
        "page": 1,
        "size": 10,
        "pages": None,
    }


################################################ Announcement


@pytest.fixture()
def announcement_db_in():
    """Fixture that returns an AnnouncementIn schema.

    Used for creating/updating an Announcement.
    """
    return schemas.AnnouncementIn(announcement_text="New Announcement", admin_id=1)


@pytest.fixture()
def announcement_db_out():
    """Fixture that returns an AnnouncementOut schema."""
    return schemas.AnnouncementOut(id=1, announcement_text="Announcement 1", admin_id=1)


@pytest.fixture()
def announcement_out():
    """Fixture that returns an announcement in dictionary."""
    return {"id": 1, "announcement_text": "Announcement 1", "admin_id": 1}


@pytest.fixture()
def announcements_out():
    """Fixture that returns a paginated list of announcements in dictionary."""
    return {
        "items": [
            {
                "id": 1,
                "announcement_text": "Announcement 1",
                "admin_id": 1,
                "name": "",
                "role": "admin",
            },
            {
                "id": 2,
                "announcement_text": "Announcement 2",
                "admin_id": 1,
                "name": "",
                "role": "admin",
            },
        ],
        "total": 2,
        "page": 1,
        "size": 10,
        "pages": None,
    }
