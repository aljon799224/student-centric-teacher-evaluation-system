"""Item repository unit tests."""

from http import HTTPStatus

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Item
from app.repositories.item import ItemRepository
from exceptions.exceptions import DatabaseException, APIException


def test_get_items(mock_session):
    """Test successful retrieval of all items."""
    mock_data = [Item(), Item()]
    mock_session.query.return_value.all.return_value = mock_data

    # Call the method
    item_repo = ItemRepository(Item)
    result = item_repo.get_all(mock_session)

    # Assertions
    mock_session.query.assert_called_once()
    assert result == mock_data


def test_get_items_exception(mock_session):
    """Test exception handling during data retrieval."""
    # Simulate a database error
    mock_session.query.side_effect = Exception("DB error")

    # Expect DatabaseException
    with pytest.raises(DatabaseException) as exc_info:
        item_repo = ItemRepository(Item)
        item_repo.get_all(mock_session)

    # Assertions
    assert exc_info.value.detail == "An error occurred while fetching the items."


def test_get_item(mock_session):
    """Test successful retrieval of a specific item."""
    mock_data = Item()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_data

    # Call the method
    item_repo = ItemRepository(Item)
    result = item_repo.get(mock_session, _id=1)

    # Assertions
    mock_session.query.assert_called_once()
    assert result == mock_data


def test_get_item_not_found(mock_session):
    """Test retrieval of an item that does not exist."""
    mock_session.query.return_value.filter.return_value.first.return_value = None

    # Expect API Exception
    with pytest.raises(APIException) as exc_info:
        item_repo = ItemRepository(Item)
        item_repo.get(mock_session, _id=1)

    # Assertions
    mock_session.query.assert_called_once()
    assert exc_info.value.detail == "Record not found."


def test_create_item_success(mock_session, item_db_in):
    """Test successful creation of an item."""
    item_repo = ItemRepository(Item)
    create_item = item_repo.create(db=mock_session, obj_in=item_db_in)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert create_item is not None
    assert create_item.name == item_db_in.name


def test_create_item_integrity_error(mock_session, item_db_in):
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
        item_repo = ItemRepository(Item)
        item_repo.create(db=mock_session, obj_in=item_db_in)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "Duplicate entry for unique constraint"
    assert exc_info.value.status_code == HTTPStatus.CONFLICT


def test_create_item_exception_error(mock_session, item_db_in):
    """Test creation with Exception error."""
    # Simulate an IntegrityError being raised when `add` is called
    mock_session.add.side_effect = Exception("error")

    # Check that DatabaseException is raised
    with pytest.raises(DatabaseException) as exc_info:
        item_repo = ItemRepository(Item)
        item_repo.create(db=mock_session, obj_in=item_db_in)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "An unexpected error occurred."
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_update_item_success(mock_session, item_db_in):
    """Test successful update of an item."""
    mock_data = Item()
    mock_data.name = "Item 2"

    item_repo = ItemRepository(Item)
    update_item = item_repo.update(db=mock_session, obj_in=item_db_in, db_obj=mock_data)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert update_item is not None
    assert update_item.name == item_db_in.name


def test_update_item_integrity_error(mock_session, item_db_in):
    """Test update with Integrity error."""
    # Simulate an IntegrityError being raised when `add` is called
    mock_session.add.side_effect = None
    mock_session.commit.side_effect = IntegrityError(
        "Simulated Integrity Error",
        orig=ValueError("Duplicate entry for unique constraint"),
        params=None,
    )

    # Check that DatabaseException is raised
    with pytest.raises(DatabaseException) as exc_info:
        item_model = Item()
        item_repo = ItemRepository(Item)
        item_repo.update(db=mock_session, obj_in=item_db_in, db_obj=item_model)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "Duplicate entry for unique constraint"
    assert exc_info.value.status_code == HTTPStatus.CONFLICT


def test_update_item_exception_error(mock_session, item_db_in):
    """Test update with Exception error."""
    # Simulate an IntegrityError being raised when `add` is called
    mock_session.add.side_effect = Exception("error")

    # Check that DatabaseException is raised
    with pytest.raises(DatabaseException) as exc_info:
        item_model = Item()
        item_repo = ItemRepository(Item)
        item_repo.update(db=mock_session, obj_in=item_db_in, db_obj=item_model)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "An unexpected error occurred during the update."
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_delete_item_success(mock_session):
    """Test delete of an item."""
    mock_data = Item()
    mock_session.query.return_value.get.return_value = mock_data

    item_repo = ItemRepository(Item)
    delete_item = item_repo.delete(db=mock_session, _id=1)

    mock_session.query.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.delete.assert_called_once()

    assert delete_item == mock_data


def test_delete_item_not_found(mock_session):
    """Test item not found during deletion."""
    mock_session.query.return_value.get.return_value = None

    with pytest.raises(APIException) as exc_info:
        item_repo = ItemRepository(Item)
        item_repo.delete(db=mock_session, _id=1)

    mock_session.query.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.delete.assert_not_called()

    assert exc_info.value.detail == "Record not found."
    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND


def test_delete_item_exception(mock_session):
    """Test item exception error during deletion."""
    mock_session.query.side_effect = Exception("error")

    with pytest.raises(DatabaseException) as exc_info:
        item_repo = ItemRepository(Item)
        item_repo.delete(db=mock_session, _id=1)

    mock_session.query.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.delete.assert_not_called()

    assert exc_info.value.detail == "An unexpected error occurred during the deletion."
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
