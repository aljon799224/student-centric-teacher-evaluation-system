"""Evaluation use case unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from fastapi_pagination import Page
from starlette.responses import JSONResponse

from app.models import Evaluation
from app.use_cases.evaluation import EvaluationUseCase
from exceptions.exceptions import DatabaseException, APIException


@patch("app.use_cases.evaluation.UserRepository", spec=True)
@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
@patch("app.use_cases.evaluation.paginate", spec=True)
def test_get_evaluations(
    m_paginate, m_repo_evaluation, m_repo_user, mock_session, user_model_out
):
    """Test get evaluations."""
    # Mock data for evaluations
    eval_1 = Evaluation()
    eval_1.title = "title 1"
    eval_1.teacher_id = 1

    eval_2 = Evaluation()
    eval_2.title = "title 2"
    eval_2.teacher_id = 2
    mock_data = [eval_1, eval_2]

    # Mock the repository calls
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.get_all.return_value = mock_data

    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.get.side_effect = [user_model_out, user_model_out]

    # Mock the paginate call
    m_paginate.return_value = Page(
        items=[
            {"teacher_name": "John Doe Doe", "title": "title 1", "teacher_id": 1},
            {"teacher_name": "John Doe Doe", "title": "title 2", "teacher_id": 2},
        ],
        total=len(mock_data),
        page=1,
        size=10,
    )

    # Create an instance of the use case
    evaluation_uc = EvaluationUseCase(db=mock_session)

    # Call the method under test
    response = evaluation_uc.get_evaluations()

    # Verify that paginate was called with the transformed data (dictionaries)
    m_paginate.assert_called_once_with(
        [
            {"teacher_name": "John Doe Doe", "title": "title 1", "teacher_id": 1},
            {"teacher_name": "John Doe Doe", "title": "title 2", "teacher_id": 2},
        ]
    )

    # Assertions to check the response matches the expected values
    assert response.items == [
        {"teacher_name": "John Doe Doe", "title": "title 1", "teacher_id": 1},
        {"teacher_name": "John Doe Doe", "title": "title 2", "teacher_id": 2},
    ]
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


@patch("app.use_cases.evaluation.UserRepository", spec=True)
@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_create_evaluation(
    m_repo_evaluation,
    m_repo_user,
    mock_session,
    evaluation_db_in,
    evaluation_model_out,
    user_model_out,
    evaluation_detailed_db_out,
):
    """Test create evaluation."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.create.return_value = evaluation_model_out

    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.get.return_value = user_model_out

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.create_evaluation(obj_in=evaluation_db_in)

    assert response == evaluation_detailed_db_out


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


@patch("app.use_cases.evaluation.UserRepository", spec=True)
@patch("app.use_cases.evaluation.EvaluationRepository", spec=True)
def test_update_evaluation(
    m_repo_evaluation,
    m_repo_user,
    mock_session,
    evaluation_db_in,
    evaluation_model_out,
    user_model_out,
    evaluation_detailed_db_out,
):
    """Test update evaluation."""
    m_repo_evaluation_instance = m_repo_evaluation.return_value
    m_repo_evaluation_instance.update.return_value = evaluation_model_out

    m_repo_user_instance = m_repo_user.return_value
    m_repo_user_instance.get.return_value = user_model_out

    evaluation_uc = EvaluationUseCase(db=mock_session)

    response = evaluation_uc.update_evaluation(_id=1, obj_in=evaluation_db_in)

    assert response == evaluation_detailed_db_out


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
