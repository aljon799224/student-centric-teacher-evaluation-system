"""Question Result Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import QuestionResult
from app.repositories.question_result import QuestionResultRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


class QuestionResultUseCase:
    """Question Result Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db."""
        self.db = db
        self.question_result_repository = QuestionResultRepository(QuestionResult)

    def get_question_results(
        self,
    ) -> Union[Page[schemas.QuestionResultOut], JSONResponse]:
        """Get all question results record."""
        try:
            question_results = self.question_result_repository.get_all(self.db)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching question results: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(question_results)

    def get_question_result(
        self, _id: int
    ) -> Union[schemas.QuestionResultOut, JSONResponse]:
        """Get question result record."""
        try:
            question_result = self.question_result_repository.get(self.db, _id)

            return schemas.QuestionResultOut.model_validate(question_result)

        except APIException as e:
            logger.error(
                f"Database error occurred while fetching question result: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def create_question_result(
        self,
        *,
        obj_in: schemas.QuestionResultIn,
    ) -> Union[schemas.QuestionResultOut, JSONResponse]:
        """Create question result record."""
        try:
            question_result = self.question_result_repository.create(
                db=self.db, obj_in=obj_in
            )
            return schemas.QuestionResultOut.model_validate(question_result)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while creating question result: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_question_result(
        self,
        *,
        _id: int,
        obj_in: schemas.QuestionResultUpdate,
    ) -> Union[schemas.QuestionResultOut, JSONResponse]:
        """Update question result record."""
        try:
            question_result = self.question_result_repository.get(db=self.db, _id=_id)

            update_question_result = self.question_result_repository.update(
                db=self.db, obj_in=obj_in, db_obj=question_result
            )
            return schemas.QuestionResultOut.model_validate(update_question_result)

        except (DatabaseException, APIException) as e:
            logger.error(
                f"Database error occurred while creating question result: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_question_result(
        self, _id: int
    ) -> Union[schemas.QuestionResultOut, JSONResponse]:
        """Delete question result record."""
        try:
            question_result_delete = self.question_result_repository.delete(
                db=self.db, _id=_id
            )

            return schemas.QuestionResultOut.model_validate(question_result_delete)

        except (DatabaseException, APIException) as e:
            logger.error(
                f"Database error occurred while deleting question result: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
