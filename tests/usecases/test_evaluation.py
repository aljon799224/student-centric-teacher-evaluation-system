"""Evaluation use case unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from fastapi_pagination import Page
from starlette.responses import JSONResponse

from app.models import Evaluation
from app.use_cases.evaluation import EvaluationUseCase
from exceptions.exceptions import DatabaseException, APIException


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
@patch("app.use_cases.evaluation.paginate", spec=True)
def test_get_evaluations(m_paginate, m_repo_evaluation, mock_session):
    """Test get evaluations."""
    mock_data = [Evaluation(), Evaluation()]
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.get_all.return_value = mock_data
    m_paginate.return_value = Page(
        items=mock_data, total=len(mock_data), page=1, size=10
    )

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.get_evaluations()
    m_paginate.assert_called_once_with(mock_data)

    assert response.items == mock_data
    assert response.total == len(mock_data)
    assert response.page == 1
    assert response.size == 10


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_get_evaluations_exception(m_repo_evaluation, mock_session):
    """Test get evaluations with exception."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.get_all.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.get_evaluations()

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_get_evaluation(m_repo_evaluation, mock_session, evaluation_db_out):
    """Test get evaluation."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.get.return_value = evaluation_db_out

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.get_evaluation(_id=1)

    assert response == evaluation_db_out


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_get_evaluation_exception(m_repo_evaluation, mock_session, evaluation_db_out):
    """Test get evaluation exception."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.get.side_effect = APIException(
        status_code=HTTPStatus.CONFLICT, detail="error"
    )

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.get_evaluation(_id=1)

    assert response.status_code == HTTPStatus.CONFLICT
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_create_evaluation(
    m_repo_evaluation,
    mock_session,
    evaluation_db_in,
    evaluation_model_out,
    evaluation_db_out,
):
    """Test create evaluation."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.create.return_value = evaluation_model_out

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.create_evaluation(obj_in=evaluation_db_in)

    assert response == evaluation_db_out


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_create_evaluation_exception(
    m_repo_evaluation, mock_session, evaluation_db_in, evaluation_db_out
):
    """Test create evaluation with exception."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.create.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.create_evaluation(obj_in=evaluation_db_in)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_update_evaluation(
    m_repo_evaluation,
    mock_session,
    evaluation_db_in,
    evaluation_db_out,
    evaluation_model_out,
):
    """Test update evaluation."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.update.return_value = evaluation_model_out

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.update_evaluation(_id=1, obj_in=evaluation_db_in)

    assert response == evaluation_db_out


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_update_evaluation_exception(
    m_repo_evaluation, mock_session, evaluation_db_in, evaluation_db_out
):
    """Test evaluation with exception."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.update.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.update_evaluation(_id=1, obj_in=evaluation_db_in)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_delete_evaluation(
    m_repo_evaluation, mock_session, evaluation_db_out, evaluation_model_out
):
    """Test delete evaluation."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.delete.return_value = evaluation_model_out

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.delete_evaluation(_id=1)

    assert response == evaluation_db_out


@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_delete_evaluation_exception(
    m_repo_evaluation, mock_session, evaluation_db_out
):
    """Test delete evaluation with exception."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.delete.side_effect = DatabaseException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="error"
    )

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.delete_evaluation(_id=1)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(response, JSONResponse)
