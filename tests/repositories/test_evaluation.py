"""Evaluation repository unit tests."""

from http import HTTPStatus

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Evaluation
from app.repositories.evaluation import EvaluationRepository
from exceptions.exceptions import DatabaseException, APIException


def test_get_evaluations(mock_session):
    """Test successful retrieval of all evaluations."""
    mock_data = [Evaluation, Evaluation]
    mock_session.query.return_value.all.return_value = mock_data

    # Call the method
    evaluation_repo = EvaluationRepository(Evaluation)
    result = evaluation_repo.get_all(mock_session)

    # Assertions
    mock_session.query.assert_called_once()
    assert result == mock_data


def test_get_evaluations_exception(mock_session):
    """Test exception handling during data retrieval."""
    # Simulate a database error
    mock_session.query.side_effect = Exception("DB error")

    # Expect DatabaseException
    with pytest.raises(DatabaseException) as exc_info:
        evaluation_repo = EvaluationRepository(Evaluation)
        evaluation_repo.get_all(mock_session)

    # Assertions
    assert exc_info.value.detail == "An error occurred while fetching the items."


def test_get_evaluation(mock_session):
    """Test successful retrieval of a specific evaluation."""
    mock_data = Evaluation
    mock_session.query.return_value.filter.return_value.first.return_value = mock_data

    # Call the method
    evaluation_repo = EvaluationRepository(Evaluation)
    result = evaluation_repo.get(mock_session, _id=1)

    # Assertions
    mock_session.query.assert_called_once()
    assert result == mock_data


def test_get_evaluation_not_found(mock_session):
    """Test retrieval of an evaluation that does not exist."""
    mock_session.query.return_value.filter.return_value.first.return_value = None

    # Expect API Exception
    with pytest.raises(APIException) as exc_info:
        evaluation_repo = EvaluationRepository(Evaluation)
        evaluation_repo.get(mock_session, _id=1)

    # Assertions
    mock_session.query.assert_called_once()
    assert exc_info.value.detail == "Record not found."


def test_create_evaluation_success(mock_session, evaluation_db_in):
    """Test successful creation of an evaluation."""
    evaluation_repo = EvaluationRepository(Evaluation)
    create_evaluation = evaluation_repo.create(db=mock_session, obj_in=evaluation_db_in)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert create_evaluation is not None
    assert create_evaluation.title == evaluation_db_in.title


def test_create_evaluation_integrity_error(mock_session, evaluation_db_in):
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
        evaluation_repo = EvaluationRepository(Evaluation)
        evaluation_repo.create(db=mock_session, obj_in=evaluation_db_in)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "Duplicate entry for unique constraint"
    assert exc_info.value.status_code == HTTPStatus.CONFLICT


def test_create_evaluation_exception_error(mock_session, evaluation_db_in):
    """Test creation with Exception error."""
    # Simulate an IntegrityError being raised when `add` is called
    mock_session.add.side_effect = Exception("error")

    # Check that DatabaseException is raised
    with pytest.raises(DatabaseException) as exc_info:
        evaluation_repo = EvaluationRepository(Evaluation)
        evaluation_repo.create(db=mock_session, obj_in=evaluation_db_in)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "An unexpected error occurred."
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_update_evaluation_success(mock_session, evaluation_db_in):
    """Test successful update of an evaluation."""
    mock_data = Evaluation()
    mock_data.title = "evaluation 2"
    mock_data.teacher_id = 1

    evaluation_repo = EvaluationRepository(Evaluation)
    update_evaluation = evaluation_repo.update(
        db=mock_session, obj_in=evaluation_db_in, db_obj=mock_data
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert update_evaluation is not None
    assert update_evaluation.title == evaluation_db_in.title


def test_update_evaluation_integrity_error(mock_session, evaluation_db_in):
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
        evaluation_model = Evaluation()
        evaluation_repo = EvaluationRepository(Evaluation)
        evaluation_repo.update(
            db=mock_session, obj_in=evaluation_db_in, db_obj=evaluation_model
        )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "Duplicate entry for unique constraint"
    assert exc_info.value.status_code == HTTPStatus.CONFLICT


def test_update_evaluation_exception_error(mock_session, evaluation_db_in):
    """Test update with Exception error."""
    # Simulate an IntegrityError being raised when `add` is called
    mock_session.add.side_effect = Exception("error")

    # Check that DatabaseException is raised
    with pytest.raises(DatabaseException) as exc_info:
        evaluation_model = Evaluation()
        evaluation_repo = EvaluationRepository(Evaluation)
        evaluation_repo.update(
            db=mock_session, obj_in=evaluation_db_in, db_obj=evaluation_model
        )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()
    assert exc_info.value.detail == "An unexpected error occurred during the update."
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_delete_evaluation_success(mock_session):
    """Test delete of an evaluation."""
    mock_data = Evaluation
    mock_session.query.return_value.get.return_value = mock_data

    evaluation_repo = EvaluationRepository(Evaluation)
    delete_evaluation = evaluation_repo.delete(db=mock_session, _id=1)

    mock_session.query.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.delete.assert_called_once()

    assert delete_evaluation == mock_data


def test_delete_evaluation_not_found(mock_session):
    """Test evaluation not found during deletion."""
    mock_session.query.return_value.get.return_value = None

    with pytest.raises(APIException) as exc_info:
        evaluation_repo = EvaluationRepository(Evaluation)
        evaluation_repo.delete(db=mock_session, _id=1)

    mock_session.query.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.delete.assert_not_called()

    assert exc_info.value.detail == "Record not found."
    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND


def test_delete_evaluation_exception(mock_session):
    """Test evaluation exception error during deletion."""
    mock_session.query.side_effect = Exception("error")

    with pytest.raises(DatabaseException) as exc_info:
        evaluation_repo = EvaluationRepository(Evaluation)
        evaluation_repo.delete(db=mock_session, _id=1)

    mock_session.query.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.delete.assert_not_called()

    assert exc_info.value.detail == "An unexpected error occurred during the deletion."
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
