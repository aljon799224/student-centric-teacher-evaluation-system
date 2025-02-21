"""Question Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import Question
from app.repositories.question import QuestionRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


class QuestionUseCase:
    """Question Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db."""
        self.db = db
        self.question_repository = QuestionRepository(Question)

    def get_questions(self) -> Union[Page[schemas.QuestionOut], JSONResponse]:
        """Get all questions record."""
        try:
            questions = self.question_repository.get_all(self.db)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching questions: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(questions)

    def get_question(self, _id: int) -> Union[schemas.QuestionOut, JSONResponse]:
        """Get question record."""
        try:
            question = self.question_repository.get(self.db, _id)

            return schemas.QuestionOut.model_validate(question)

        except APIException as e:
            logger.error(f"Database error occurred while fetching question: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def create_question(
        self,
        *,
        obj_in: schemas.QuestionIn,
    ) -> Union[schemas.QuestionOut, JSONResponse]:
        """Create question record."""
        try:
            question = self.question_repository.create(db=self.db, obj_in=obj_in)
            return schemas.QuestionOut.model_validate(question)

        except DatabaseException as e:
            logger.error(f"Database error occurred while creating question: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_question(
        self,
        *,
        _id: int,
        obj_in: schemas.QuestionUpdate,
    ) -> Union[schemas.QuestionOut, JSONResponse]:
        """Update question record."""
        try:
            question = self.question_repository.get(db=self.db, _id=_id)

            update_question = self.question_repository.update(
                db=self.db, obj_in=obj_in, db_obj=question
            )
            return schemas.QuestionOut.model_validate(update_question)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while creating question: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_question(self, _id: int) -> Union[schemas.QuestionOut, JSONResponse]:
        """Delete question record."""
        try:
            question_update = self.question_repository.delete(db=self.db, _id=_id)

            return schemas.QuestionOut.model_validate(question_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while deleting question: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
