"""User repository unit tests."""

from http import HTTPStatus
from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.security import verify_password
from app.models import User
from app.repositories.user import UserRepository
from exceptions.exceptions import DatabaseException


def test_get_by_username(mock_session):
    """Test successful retrieval user by username."""
    mock_data = User()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_data

    # Call the method
    user_repo = UserRepository(User)
    result = user_repo.get_by_username(mock_session, username="user1")

    # Assertions
    mock_session.query.assert_called_once()
    assert result == mock_data


def test_create_user_success(mock_session, user_db_in):
    """Test successful creation of a user."""
    user_repo = UserRepository(User)
    create_user = user_repo.create_user_with_password(
        db=mock_session, obj_in=user_db_in
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert create_user is not None
    assert create_user.username == user_db_in.username
    assert verify_password(user_db_in.password, create_user.hashed_password)


def test_create_user_integrity_error(mock_session, user_db_in):
    """Test creation with Integrity error."""
    # Simulate an IntegrityError being raised when `add` is called
    mock_session.add.side_effect = None
    mock_session.commit.side_effect = IntegrityError(
        "Simulated Integrity Error",
        orig=ValueError("Duplicate entry for unique constraint"),
        params=None,
    )

    # Check that DatabaseException is raised
    with pytest.raises(DatabaseException) as exc_info:
        user_repo = UserRepository(User)
        user_repo.create_user_with_password(db=mock_session, obj_in=user_db_in)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "Duplicate entry for unique constraint"
    assert exc_info.value.status_code == HTTPStatus.CONFLICT


def test_create_user_exception_error(mock_session, user_db_in):
    """Test creation with Exception error."""
    # Simulate an IntegrityError being raised when `add` is called
    mock_session.add.side_effect = Exception("error")

    # Check that DatabaseException is raised
    with pytest.raises(DatabaseException) as exc_info:
        user_repo = UserRepository(User)
        user_repo.create_user_with_password(db=mock_session, obj_in=user_db_in)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "An unexpected error occurred."
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@patch("app.repositories.user.verify_password", spec=True)
def test_authenticate(m_verify_password, mock_session):
    """Test successful authentication of a user."""
    mock_data = User()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_data

    m_verify_password.return_value = True

    # Call the method
    user_repo = UserRepository(User)
    result = user_repo.authenticate(mock_session, username="user", password="password")

    # Assertions
    mock_session.query.assert_called_once()
    assert result == mock_data


@patch("app.repositories.user.verify_password", spec=True)
def test_authenticate_no_user(m_verify_password, mock_session):
    """Test successful authentication of a user."""
    mock_session.query.return_value.filter.return_value.first.return_value = None

    m_verify_password.return_value = True

    # Call the method
    user_repo = UserRepository(User)
    result = user_repo.authenticate(mock_session, username="user", password="password")

    # Assertions
    mock_session.query.assert_called_once()
    assert result is None


@patch("app.repositories.user.verify_password", spec=True)
def test_authenticate_wrong_password(m_verify_password, mock_session):
    """Test successful authentication of a user."""
    mock_data = User()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_data

    m_verify_password.return_value = False

    # Call the method
    user_repo = UserRepository(User)
    result = user_repo.authenticate(mock_session, username="user", password="password")

    # Assertions
    mock_session.query.assert_called_once()
    assert result is None
