"""Item use case unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from fastapi_pagination import Page
from starlette.responses import JSONResponse

from app.models import Item
from app.use_cases.item import ItemUseCase
from exceptions.exceptions import DatabaseException, APIException


@patch("app.use_cases.item.ItemRepository", spec=True)
@patch("app.use_cases.item.paginate", spec=True)
def test_get_items(m_paginate, m_repo_item, mock_session):
    """Test get items."""
    mock_data = [Item(), Item()]
    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.get_all.return_value = mock_data
    m_paginate.return_value = Page(
        items=mock_data, total=len(mock_data), page=1, size=10
    )

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.get_items()
    m_paginate.assert_called_once_with(mock_data)

    assert response.items == mock_data
    assert response.total == len(mock_data)
    assert response.page == 1
    assert response.size == 10


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_get_items_exception(m_repo_item, mock_session):
    """Test get items with exception."""
    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.get_all.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.get_items()

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_get_item(m_repo_item, mock_session, item_db_out):
    """Test get item."""
    mock_data = Item()
    mock_data.id = 1
    mock_data.name = "Item 1"
    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.get.return_value = mock_data

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.get_item(_id=1)

    assert response == item_db_out


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_get_item_exception(m_repo_item, mock_session, item_db_out):
    """Test get item exception."""
    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.get.side_effect = APIException(
        status_code=HTTPStatus.CONFLICT, detail="error"
    )

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.get_item(_id=1)

    assert response.status_code == HTTPStatus.CONFLICT
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_create_item(m_repo_item, mock_session, item_db_in, item_db_out):
    """Test create item."""
    mock_data = Item()
    mock_data.id = 1
    mock_data.name = "Item 1"

    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.create.return_value = mock_data

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.create_item(obj_in=item_db_in)

    assert response == item_db_out


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_create_item_exception(m_repo_item, mock_session, item_db_in, item_db_out):
    """Test create item with exception."""
    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.create.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.create_item(obj_in=item_db_in)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_update_item(m_repo_item, mock_session, item_db_in, item_db_out):
    """Test update item."""
    mock_data = Item()
    mock_data.id = 1
    mock_data.name = "Item 1"

    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.update.return_value = mock_data

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.update_item(_id=1, obj_in=item_db_in)

    assert response == item_db_out


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_update_item_exception(m_repo_item, mock_session, item_db_in, item_db_out):
    """Test item with exception."""
    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.update.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.update_item(_id=1, obj_in=item_db_in)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_delete_item(m_repo_item, mock_session, item_db_out):
    """Test delete item."""
    mock_data = Item()
    mock_data.id = 1
    mock_data.name = "Item 1"

    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.delete.return_value = mock_data

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.delete_item(_id=1)

    assert response == item_db_out


@patch("app.use_cases.item.ItemRepository", spec=True)
def test_delete_item_exception(m_repo_item, mock_session, item_db_out):
    """Test delete item with exception."""
    m_repo_item_instance = m_repo_item.return_value
    m_repo_item_instance.delete.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    item_uc = ItemUseCase(db=mock_session)

    response = item_uc.delete_item(_id=1)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)
