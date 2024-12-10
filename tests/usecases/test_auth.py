"""Auth use case unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.models import User
from app.use_cases.auth import AuthenticationUseCase


@patch("app.use_cases.auth.UserRepository", spec=True)
def test_login_access_token(
    m_repo_user,
    mock_session,
    form_data_in_for_login_access_token,
    login_access_token_out,
    user_model_out,
):
    """Test login access token."""
    mock_data = User()

    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.authenticate.return_value = mock_data

    user_uc = AuthenticationUseCase(db=mock_session)

    response = user_uc.login_access_token(
        form_data=OAuth2PasswordRequestForm(username="user", password="password")
    )

    assert "access_token" in response
    assert response["token_type"] == "bearer"


@patch("app.use_cases.auth.create_access_token", spec=True)
@patch("app.use_cases.auth.UserRepository", spec=True)
def test_login_access_token_no_user(
    m_repo_user,
    mock_session,
    form_data_in_for_login_access_token,
    login_access_token_out,
    user_model_out,
):
    """Test login access token no user."""
    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.authenticate.return_value = None

    user_uc = AuthenticationUseCase(db=mock_session)

    response = user_uc.login_access_token(
        form_data=OAuth2PasswordRequestForm(username="user", password="password")
    )

    assert isinstance(response, JSONResponse)
    assert response.status_code == HTTPStatus.NOT_FOUND
