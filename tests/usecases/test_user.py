"""User use case unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from fastapi_pagination import Page
from starlette.responses import JSONResponse

from app.models import User
from app.use_cases.user import UserUseCase
from exceptions.exceptions import DatabaseException, APIException


@patch("app.use_cases.user.UserRepository", spec=True)
@patch("app.use_cases.user.paginate", spec=True)
def test_get_users(m_paginate, m_repo_user, mock_session):
    """Test get users."""
    user_1 = User()
    user_1.email = "user@yahoo.com"
    user_1.username = "user"

    user_2 = User()
    user_2.email = "user2@yahoo.com"
    user_2.username = "user2"

    mock_data = [user_1, user_2]

    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.get_all.return_value = mock_data
    m_paginate.return_value = Page(
        items=mock_data, total=len(mock_data), page=1, size=10
    )

    user_uc = UserUseCase(db=mock_session)

    response = user_uc.get_users()
    m_paginate.assert_called_once_with(mock_data)

    assert response.items == mock_data
    assert response.total == len(mock_data)
    assert response.page == 1
    assert response.size == 10


@patch("app.use_cases.user.UserRepository", spec=True)
def test_get_users_exception(m_repo_user, mock_session):
    """Test get users with exception."""
    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.get_all.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    user_uc = UserUseCase(db=mock_session)

    response = user_uc.get_users()

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.user.UserRepository", spec=True)
def test_get_user(m_repo_user, mock_session, user_db_out, user_model_out):
    """Test get user."""
    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.get.return_value = user_model_out

    user_uc = UserUseCase(db=mock_session)

    response = user_uc.get_user(_id=1)

    assert response == user_db_out


@patch("app.use_cases.user.UserRepository", spec=True)
def test_get_user_exception(m_repo_user, mock_session, user_db_out):
    """Test get user exception."""
    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.get.side_effect = APIException(
        status_code=HTTPStatus.CONFLICT, detail="error"
    )

    user_uc = UserUseCase(db=mock_session)

    response = user_uc.get_user(_id=1)

    assert response.status_code == HTTPStatus.CONFLICT
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.user.UserRepository", spec=True)
def test_create_user(
    m_repo_user, mock_session, user_db_in, user_db_out, user_model_out
):
    """Test create user."""
    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.create_user_with_password.return_value = user_model_out

    user_uc = UserUseCase(db=mock_session)

    response = user_uc.create_user(obj_in=user_db_in)

    assert response == user_db_out


@patch("app.use_cases.user.UserRepository", spec=True)
def test_create_user_exception(m_repo_user, mock_session, user_db_in, user_db_out):
    """Test create user with exception."""
    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.create_user_with_password.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    user_uc = UserUseCase(db=mock_session)

    response = user_uc.create_user(obj_in=user_db_in)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.user.UserRepository", spec=True)
def test_delete_user(m_repo_user, mock_session, user_db_out, user_model_out):
    """Test delete user."""
    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.delete.return_value = user_model_out

    user_uc = UserUseCase(db=mock_session)

    response = user_uc.delete_user(_id=1)

    assert response == user_db_out


@patch("app.use_cases.user.UserRepository", spec=True)
def test_delete_user_exception(m_repo_user, mock_session, user_db_out):
    """Test delete user with exception."""
    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.delete.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    user_uc = UserUseCase(db=mock_session)

    response = user_uc.delete_user(_id=1)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)
