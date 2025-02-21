"""Announcement use case unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from fastapi_pagination import Page
from starlette.responses import JSONResponse

from app.models import Announcement
from app.use_cases.announcement import AnnouncementUseCase
from exceptions.exceptions import DatabaseException, APIException


@patch("app.use_cases.evaluation.UserRepository", spec=True)
@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
@patch("app.use_cases.announcement.paginate", spec=True)
def test_get_announcements(
    m_paginate, m_repo_announcement, m_repo_user, mock_session, user_model_out
):
    """Test get announcements."""
    mock_data = [Announcement(), Announcement()]

    announcement_1 = Announcement()
    announcement_1.announcement_text = "Announcement 1"
    announcement_1.admin_id = 1

    announcement_2 = Announcement()
    announcement_2.announcement_text = "Announcement 2"
    announcement_2.admin_id = 2
    mock_data = [announcement_1, announcement_2]

    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.get_all.return_value = mock_data

    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.get.side_effect = [user_model_out, user_model_out]

    # Mock the paginate call
    m_paginate.return_value = Page(
        items=[
            {
                "role": "admin",
                "announcement_text": "Announcement 1",
                "admin_id": 1,
                "name": "Admin John Doe",
            },
            {
                "role": "admin",
                "announcement_text": "Announcement 2",
                "admin_id": 1,
                "name": "Admin John Doe",
            },
        ],
        total=len(mock_data),
        page=1,
        size=10,
    )

    # Create an instance of the use case
    announcement_uc = AnnouncementUseCase(db=mock_session)

    # Call the method under test
    response = announcement_uc.get_announcements()

    # Verify that paginate was called with the transformed data (dictionaries)
    # m_paginate.assert_called_once_with(
    #     [
    #         {
    #         "role": "admin",
    #         "announcement_text": "Announcement 1",
    #         "admin_id": 1, 'name': 'Admin John Doe'},
    #         {"role": "admin", "announcement_text":
    #         "Announcement 2", "admin_id": 1, 'name':
    #         'Admin John Doe'},
    #     ]
    # )

    # Assertions to check the response matches the expected values
    assert response.items == [
        {
            "role": "admin",
            "announcement_text": "Announcement 1",
            "admin_id": 1,
            "name": "Admin John Doe",
        },
        {
            "role": "admin",
            "announcement_text": "Announcement 2",
            "admin_id": 1,
            "name": "Admin John Doe",
        },
    ]
    assert response.total == len(mock_data)
    assert response.page == 1
    assert response.size == 10


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_get_announcements_exception(m_repo_announcement, mock_session):
    """Test get announcements with exception."""
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.get_all.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.get_announcements()

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_get_announcement(m_repo_announcement, mock_session, announcement_db_out):
    """Test get announcement."""
    mock_data = Announcement()
    mock_data.id = 1
    mock_data.announcement_text = "Announcement 1"
    mock_data.admin_id = 1
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.get.return_value = mock_data

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.get_announcement(_id=1)

    assert response == announcement_db_out


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_get_announcement_exception(
    m_repo_announcement, mock_session, announcement_db_out
):
    """Test get announcement exception."""
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.get.side_effect = APIException(
        status_code=HTTPStatus.CONFLICT, detail="error"
    )

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.get_announcement(_id=1)

    assert response.status_code == HTTPStatus.CONFLICT
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_create_announcement(
    m_repo_announcement, mock_session, announcement_db_in, announcement_db_out
):
    """Test create announcement."""
    mock_data = Announcement()
    mock_data.id = 1
    mock_data.announcement_text = "Announcement 1"
    mock_data.admin_id = 1
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.create.return_value = mock_data

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.create_announcement(obj_in=announcement_db_in)

    assert response == announcement_db_out


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_create_announcement_exception(
    m_repo_announcement, mock_session, announcement_db_in, announcement_db_out
):
    """Test create announcement with exception."""
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.create.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.create_announcement(obj_in=announcement_db_in)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_update_announcement(
    m_repo_announcement, mock_session, announcement_db_in, announcement_db_out
):
    """Test update announcement."""
    mock_data = Announcement()
    mock_data.id = 1
    mock_data.announcement_text = "Announcement 1"
    mock_data.admin_id = 1
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.update.return_value = mock_data

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.update_announcement(_id=1, obj_in=announcement_db_in)

    assert response == announcement_db_out


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_update_announcement_exception(
    m_repo_announcement, mock_session, announcement_db_in, announcement_db_out
):
    """Test announcement with exception."""
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.update.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.update_announcement(_id=1, obj_in=announcement_db_in)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_delete_announcement(m_repo_announcement, mock_session, announcement_db_out):
    """Test delete announcement."""
    mock_data = Announcement()
    mock_data.id = 1
    mock_data.announcement_text = "Announcement 1"
    mock_data.admin_id = 1
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.delete.return_value = mock_data

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.delete_announcement(_id=1)

    assert response == announcement_db_out


@patch("app.use_cases.announcement.AnnouncementRepository", spec=True)
def test_delete_announcement_exception(
    m_repo_announcement, mock_session, announcement_db_out
):
    """Test delete announcement with exception."""
    m_repo_announcement_instance = m_repo_announcement.return_value
    m_repo_announcement_instance.delete.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    announcement_uc = AnnouncementUseCase(db=mock_session)

    response = announcement_uc.delete_announcement(_id=1)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)
