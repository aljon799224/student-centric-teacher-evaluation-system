"""Question Endpoint."""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.question import QuestionUseCase

question_router = APIRouter()


@question_router.get("/question", response_model=Page[schemas.QuestionOut])
def get_questions(
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Get all questions."""
    question_uc = QuestionUseCase(db=db)

    questions = question_uc.get_questions()

    return questions


@question_router.get("/question/{_id}", response_model=schemas.QuestionOut)
def get_question(
    _id: int,
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Get question by ID."""
    question_uc = QuestionUseCase(db=db)

    question = question_uc.get_question(_id=_id)

    return question


@question_router.post("/question", response_model=schemas.QuestionOut)
def create(
    obj_in: schemas.QuestionIn,
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Create question."""
    question_uc = QuestionUseCase(db=db)

    question = question_uc.create_question(obj_in=obj_in)

    return question


@question_router.put("/question/{_id}", response_model=schemas.QuestionOut)
def update(
    _id: int,
    obj_in: schemas.QuestionUpdate,
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Update question."""
    question_uc = QuestionUseCase(db=db)

    question = question_uc.update_question(_id=_id, obj_in=obj_in)

    return question


@question_router.delete("/question/{_id}", response_model=schemas.QuestionOut)
def delete(
    _id: int,
    db: Session = Depends(get_db),
    current_question: models.Question = Depends(get_current_active_user),
):
    """Delete question by ID."""
    question_uc = QuestionUseCase(db=db)

    question = question_uc.delete_question(_id=_id)

    return question
