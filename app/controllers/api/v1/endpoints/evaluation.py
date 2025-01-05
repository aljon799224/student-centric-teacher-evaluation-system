"""Evaluation Endpoint."""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.evaluation import EvaluationUseCase

evaluation_router = APIRouter()


@evaluation_router.get("/evaluation", response_model=Page[schemas.EvaluationOut])
def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all evaluations."""
    evaluation_uc = EvaluationUseCase(db=db)

    evaluations = evaluation_uc.get_evaluations()

    return evaluations


@evaluation_router.get("/evaluation/{_id}", response_model=schemas.EvaluationOut)
def get(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get evaluation by ID."""
    evaluation_uc = EvaluationUseCase(db=db)

    evaluation = evaluation_uc.get_evaluation(_id=_id)

    return evaluation


@evaluation_router.post("/evaluation", response_model=schemas.EvaluationOut)
def create(obj_in: schemas.EvaluationIn, db: Session = Depends(get_db)):
    """Create evaluation."""
    evaluation_uc = EvaluationUseCase(db=db)

    evaluation = evaluation_uc.create_evaluation(obj_in=obj_in)

    return evaluation


@evaluation_router.put("/evaluation/{_id}", response_model=schemas.EvaluationOut)
def update(_id: int, obj_in: schemas.EvaluationUpdate, db: Session = Depends(get_db)):
    """Update Evaluation."""
    evaluation_uc = EvaluationUseCase(db=db)

    evaluation = evaluation_uc.update_evaluation(_id=_id, obj_in=obj_in)

    return evaluation


@evaluation_router.delete("/evaluation/{_id}", response_model=schemas.EvaluationOut)
def delete(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Delete evaluation by ID."""
    evaluation_uc = EvaluationUseCase(db=db)

    evaluation = evaluation_uc.delete_evaluation(_id=_id)

    return evaluation
