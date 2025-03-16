"""Evaluation Result Endpoint."""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.evaluation_result import EvaluationResultUseCase

evaluation_result_router = APIRouter()


@evaluation_result_router.get(
    "/evaluation-result", response_model=Page[schemas.EvaluationsResultOut]
)
def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all evaluations results."""
    evaluation_uc = EvaluationResultUseCase(db=db)

    evaluations = evaluation_uc.get_evaluation_results()

    return evaluations


@evaluation_result_router.get(
    "/{evaluation_id}/{admin_id}/evaluation-result",
    response_model=Page[schemas.EvaluationsOut],
)
def get_all_by_evaluation_and_admin_id(
    evaluation_id: int,
    admin_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all evaluation results by evaluation id ad admin id."""
    evaluation_uc = EvaluationResultUseCase(db=db)

    evaluations = evaluation_uc.get_evaluation_results_by_evaluation_and_admin_id(
        evaluation_id=evaluation_id, admin_id=admin_id
    )

    return evaluations


@evaluation_result_router.get(
    "/{evaluation_id}/evaluation-result",
    response_model=Page[schemas.EvaluationDetailedResultOut],
)
def get_all_by_evaluation_id(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all evaluation results by evaluation id."""
    evaluation_uc = EvaluationResultUseCase(db=db)

    evaluations = evaluation_uc.get_evaluation_results_by_evaluation_id(
        evaluation_id=evaluation_id
    )

    return evaluations


@evaluation_result_router.get(
    "/evaluation-result/teacher/{teacher_id}",
    response_model=Page[schemas.EvaluationDetailedResultOut],
)
def get_all_by_teacher_id(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all evaluation results by teacher id"""
    evaluation_uc = EvaluationResultUseCase(db=db)
    print("--------asdasd")
    evaluations = evaluation_uc.get_evaluation_results_by_teacher_id(
        teacher_id=teacher_id
    )

    return evaluations



@evaluation_result_router.get(
    "/evaluation-result/{_id}", response_model=schemas.EvaluationOut
)
def get(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get evaluation result by ID."""
    evaluation_uc = EvaluationResultUseCase(db=db)

    evaluation = evaluation_uc.get_evaluation_result(_id=_id)

    return evaluation


@evaluation_result_router.post(
    "/evaluation-result", response_model=schemas.EvaluationDetailedResultOut
)
def create(
    obj_in: schemas.EvaluationResultIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Create evaluation result."""
    evaluation_uc = EvaluationResultUseCase(db=db)

    evaluation = evaluation_uc.create_evaluation_result(obj_in=obj_in)

    return evaluation


@evaluation_result_router.put(
    "/evaluation-result/{_id}", response_model=schemas.EvaluationDetailedOut
)
def update(
    _id: int,
    obj_in: schemas.EvaluationResultUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Update Evaluation Result."""
    evaluation_uc = EvaluationResultUseCase(db=db)

    evaluation = evaluation_uc.update_evaluation_result(_id=_id, obj_in=obj_in)

    return evaluation


@evaluation_result_router.delete(
    "/evaluation-result/{_id}", response_model=schemas.EvaluationOut
)
def delete(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Delete evaluation result by ID."""
    evaluation_uc = EvaluationResultUseCase(db=db)

    evaluation = evaluation_uc.delete_evaluation(_id=_id)

    return evaluation
