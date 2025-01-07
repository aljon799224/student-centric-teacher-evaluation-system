"""Evaluation endpoint unit tests."""

from http import HTTPStatus
from unittest.mock import patch

from app.core.config import settings
from tests.controllers.api.v1.endpoints import test_client


@patch("app.controllers.api.v1.endpoints.evaluation.EvaluationUseCase", spec=True)
def test_get_evaluations(m_evaluation_uc, evaluations_out):
    """Test gel all evaluations."""
    m_evaluation_uc_instance = m_evaluation_uc.return_value
    m_evaluation_uc_instance.get_evaluations.return_value = evaluations_out

    response = test_client.get(
        f"{settings.API_PREFIX}/evaluation",
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == evaluations_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.evaluation.EvaluationUseCase", spec=True)
def test_get_evaluation(m_evaluation_uc, evaluation_db_out, evaluation_out):
    """Test gel evaluation."""
    m_evaluation_uc_instance = m_evaluation_uc.return_value
    m_evaluation_uc_instance.get_evaluation.return_value = evaluation_db_out

    response = test_client.get(
        f"{settings.API_PREFIX}/evaluation/1",
        params={"_id": 1},
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == evaluation_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.evaluation.EvaluationUseCase", spec=True)
def test_create_evaluation(
    m_evaluation_uc,
    evaluation_db_in,
    evaluation_detailed_db_out,
    evaluation_detailed_out,
):
    """Test create evaluation."""
    m_evaluation_uc_instance = m_evaluation_uc.return_value
    m_evaluation_uc_instance.create_evaluation.return_value = evaluation_detailed_db_out

    evaluation_db_in_serialized = evaluation_db_in.model_dump()
    evaluation_db_in_serialized["created_at"] = evaluation_db_in_serialized[
        "created_at"
    ].isoformat()
    evaluation_db_in_serialized["updated_at"] = evaluation_db_in_serialized[
        "updated_at"
    ].isoformat()

    response = test_client.post(
        f"{settings.API_PREFIX}/evaluation",
        json=evaluation_db_in_serialized,
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == evaluation_detailed_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.evaluation.EvaluationUseCase", spec=True)
def test_delete_evaluation(m_evaluation_uc, evaluation_db_out, evaluation_out):
    """Test delete evaluation."""
    m_evaluation_uc_instance = m_evaluation_uc.return_value
    m_evaluation_uc_instance.delete_evaluation.return_value = evaluation_db_out

    response = test_client.delete(
        f"{settings.API_PREFIX}/evaluation/1",
        params={"_id": 1},
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == evaluation_out
    assert response.status_code == HTTPStatus.OK


@patch("app.controllers.api.v1.endpoints.evaluation.EvaluationUseCase", spec=True)
def test_update_evaluation(
    m_evaluation_uc,
    evaluation_db_in,
    evaluation_detailed_db_out,
    evaluation_detailed_out,
):
    """Test update evaluation."""
    m_evaluation_uc_instance = m_evaluation_uc.return_value
    m_evaluation_uc_instance.update_evaluation.return_value = evaluation_detailed_db_out

    evaluation_db_in_serialized = evaluation_db_in.model_dump()
    evaluation_db_in_serialized["created_at"] = evaluation_db_in_serialized[
        "created_at"
    ].isoformat()
    evaluation_db_in_serialized["updated_at"] = evaluation_db_in_serialized[
        "updated_at"
    ].isoformat()

    response = test_client.put(
        f"{settings.API_PREFIX}/evaluation/1",
        json=evaluation_db_in_serialized,
        headers={"Authorization": "Bearer TEST_TOKEN"},
    )

    assert response.json() == evaluation_detailed_out
    assert response.status_code == HTTPStatus.OK
