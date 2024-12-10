"""User endpoint unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from app.core.config import settings
from tests.controllers.api.v1.endpoints import test_client


@patch("app.controllers.api.v1.endpoints.user.UserUseCase", spec=True)
def test_get_users(m_user_uc, users_out):
    """Test gel all users."""
    m_user_uc_instance = m_user_uc.return_value
    m_user_uc_instance.get_users.return_value = users_out

    response = test_client.get(
        f"{settings.API_PREFIX}/user", headers={"Authorization": "Bearer TEST_TOKEN"}
    )

    assert response.json() == users_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.user.UserUseCase", spec=True)
def test_get_user(m_user_uc, user_db_out, user_out):
    """Test gel user."""
    m_user_uc_instance = m_user_uc.return_value
    m_user_uc_instance.get_user.return_value = user_db_out

    response = test_client.get(
        f"{settings.API_PREFIX}/user/1",
        params={"_id": 1},
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == user_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.user.UserUseCase", spec=True)
def test_create_user(m_user_uc, user_db_in, user_db_out, user_out):
    """Test create user."""
    m_user_uc_instance = m_user_uc.return_value
    m_user_uc_instance.create_user.return_value = user_db_out

    response = test_client.post(f"{settings.API_PREFIX}/user", json=user_db_in.dict())

    assert response.json() == user_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.user.UserUseCase", spec=True)
def test_delete_user(m_user_uc, user_db_out, user_out):
    """Test delete user."""
    m_user_uc_instance = m_user_uc.return_value
    m_user_uc_instance.delete_user.return_value = user_db_out

    response = test_client.delete(
        f"{settings.API_PREFIX}/user/1",
        params={"_id": 1},
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == user_out
    assert response.status_code == HTTPStatus.OK
