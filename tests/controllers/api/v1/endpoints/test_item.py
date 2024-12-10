"""Item endpoint unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from app.core.config import settings
from tests.controllers.api.v1.endpoints import test_client


@patch("app.controllers.api.v1.endpoints.item.ItemUseCase", spec=True)
def test_get_items(m_item_uc, items_out):
    """Test gel all items."""
    m_item_uc_instance = m_item_uc.return_value
    m_item_uc_instance.get_items.return_value = items_out

    response = test_client.get(
        f"{settings.API_PREFIX}/item", headers={"Authorization": "Bearer TEST_TOKEN"}
    )

    assert response.json() == items_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.item.ItemUseCase", spec=True)
def test_get_item(item_uc, item_db_out, item_out):
    """Test gel item."""
    item_uc_instance = item_uc.return_value
    item_uc_instance.get_item.return_value = item_db_out

    response = test_client.get(
        f"{settings.API_PREFIX}/item/1",
        params={"_id": 1},
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == item_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.item.ItemUseCase", spec=True)
def test_create_item(item_uc, item_db_out, item_out):
    """Test create item."""
    item_uc_instance = item_uc.return_value
    item_uc_instance.create_item.return_value = item_db_out

    response = test_client.post(
        f"{settings.API_PREFIX}/item",
        json={"name": "Updated item"},
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == item_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.item.ItemUseCase", spec=True)
def test_update_item(item_uc, item_db_out, item_out):
    """Test update item."""
    item_uc_instance = item_uc.return_value
    item_uc_instance.update_item.return_value = item_db_out

    response = test_client.put(
        f"{settings.API_PREFIX}/item?_id=1",
        json={"name": "Updated item"},
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == item_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.item.ItemUseCase", spec=True)
def test_delete_item(item_uc, item_db_out, item_out):
    """Test delete item."""
    item_uc_instance = item_uc.return_value
    item_uc_instance.delete_item.return_value = item_db_out

    response = test_client.delete(
        f"{settings.API_PREFIX}/item/1",
        params={"_id": 1},
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == item_out
    assert response.status_code == HTTPStatus.OK
