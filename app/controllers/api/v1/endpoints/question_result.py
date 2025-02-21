"""Question Result Endpoint."""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.question_result import QuestionResultUseCase

question_result_router = APIRouter()


@question_result_router.get(
    "/question-result", response_model=Page[schemas.QuestionOut]
)
def get_question_results(
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Get all question results."""
    question_uc = QuestionResultUseCase(db=db)

    questions = question_uc.get_question_results()

    return questions


@question_result_router.get(
    "/question-result/{_id}", response_model=schemas.QuestionOut
)
def get_question_result(
    _id: int,
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Get question result by ID."""
    question_uc = QuestionResultUseCase(db=db)

    question = question_uc.get_question_result(_id=_id)

    return question


@question_result_router.post("/question-result", response_model=schemas.QuestionOut)
def create(
    obj_in: schemas.QuestionResultIn,
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Create question result."""
    question_uc = QuestionResultUseCase(db=db)

    question = question_uc.create_question_result(obj_in=obj_in)

    return question


@question_result_router.put(
    "/question-result/{_id}", response_model=schemas.QuestionOut
)
def update(
    _id: int,
    obj_in: schemas.QuestionResultUpdate,
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Update question."""
    question_uc = QuestionResultUseCase(db=db)

    question = question_uc.update_question_result(_id=_id, obj_in=obj_in)

    return question


@question_result_router.delete(
    "/question-result/{_id}", response_model=schemas.QuestionOut
)
def delete(
    _id: int,
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Delete question result by ID."""
    question_uc = QuestionResultUseCase(db=db)

    question = question_uc.delete_question_result(_id=_id)

    return question
