"""Conftest."""

from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app import schemas
from app.models import User


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
    mock_data.middle_name = "Bean"
    mock_data.last_name = "Doe"
    mock_data.disabled = True

    return mock_data


@pytest.fixture()
def user_db_in():
    """Fixture that returns a UserIn schema for creating/updating an item."""
    return schemas.UserIn(
        username="User 1",
        email="user@yahoo.com",
        first_name="John",
        middle_name="Bean",
        last_name="Doe",
        disabled=True,
        password="password",
    )


@pytest.fixture()
def user_db_out():
    """Fixture that returns a UserOut schema."""
    return schemas.UserOut(
        id=1,
        username="User 1",
        email="user@yahoo.com",
        first_name="John",
        middle_name="Bean",
        last_name="Doe",
        disabled=True,
        password="password",
    )


@pytest.fixture()
def user_out():
    """Fixture that returns a user in dictionary."""
    return {
        "id": 1,
        "username": "User 1",
        "email": "user@yahoo.com",
        "first_name": "John",
        "middle_name": "Bean",
        "last_name": "Doe",
        "disabled": True,
    }


@pytest.fixture()
def users_out():
    """Fixture that returns a paginated list of users in dictionary."""
    return {
        "items": [
            {
                "id": 1,
                "username": "User 1",
                "email": "user@yahoo.com",
                "first_name": "John",
                "middle_name": "Bean",
                "last_name": "Doe",
                "disabled": True,
            },
            {
                "id": 2,
                "username": "User 2",
                "email": "user2@yahoo.com",
                "first_name": "Jane",
                "middle_name": "Bean",
                "last_name": "Doe",
                "disabled": True,
            },
        ],
        "total": 2,
        "page": 1,
        "size": 10,
        "pages": None,
    }
