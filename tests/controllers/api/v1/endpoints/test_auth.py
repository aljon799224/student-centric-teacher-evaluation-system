"""Auth endpoint unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from app.core.config import settings
from tests.controllers.api.v1.endpoints import test_client


@patch("app.controllers.api.v1.endpoints.auth.AuthenticationUseCase", spec=True)
def test_login_access_token(
    m_auth_uc, login_access_token_out, form_data_in_for_login_access_token
):
    """Test login access token."""
    m_auth_uc_instance = m_auth_uc.return_value
    m_auth_uc_instance.login_access_token.return_value = login_access_token_out

    response = test_client.post(
        f"{settings.API_PREFIX}/auth/login/token",
        data=form_data_in_for_login_access_token,
    )

    assert response.json() == login_access_token_out
    assert response.status_code == HTTPStatus.OK
