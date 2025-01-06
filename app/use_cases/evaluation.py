"""Evaluation Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import Evaluation, User
from app.repositories.evaluation import EvaluationRepository
from app.repositories.user import UserRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


# TBC Update function
class EvaluationUseCase:
    """Evaluation Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db."""
        self.db = db
        self.evaluation_repository = EvaluationRepository(Evaluation)
        self.user_repository = UserRepository(User)

    def get_evaluations(self) -> Union[Page[schemas.EvaluationsOut], JSONResponse]:
        """Get all evaluations record."""
        try:
            response = []

            evaluations = self.evaluation_repository.get_all(self.db)

            for evaluation in evaluations:
                user = self.user_repository.get(self.db, evaluation.teacher_id)

                evaluation_dict = {
                    key: value
                    for key, value in vars(evaluation).items()
                    if not key.startswith("_")
                }

                full_name = f"{user.first_name} {user.middle_name} {user.last_name}"
                evaluation_dict.update({"teacher_name": full_name})

                response.append(evaluation_dict)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching evaluations: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(response)

    def get_evaluation(self, _id: int) -> Union[schemas.EvaluationOut, JSONResponse]:
        """Get evaluation record."""
        try:
            evaluation = self.evaluation_repository.get(self.db, _id)

            return schemas.EvaluationOut.model_validate(evaluation)

        except APIException as e:
            logger.error(
                f"Database error occurred while fetching evaluation: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def create_evaluation(
        self,
        *,
        obj_in: schemas.EvaluationIn,
    ) -> Union[schemas.EvaluationOut, JSONResponse]:
        """Create evaluation record."""
        try:
            evaluation = self.evaluation_repository.create(db=self.db, obj_in=obj_in)
            return schemas.EvaluationOut.model_validate(evaluation)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while creating evaluation: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_evaluation(
        self,
        *,
        _id: int,
        obj_in: schemas.EvaluationUpdate,
    ) -> Union[schemas.EvaluationOut, JSONResponse]:
        """Update evaluation record."""
        try:
            evaluation = self.evaluation_repository.get(db=self.db, _id=_id)

            update_evaluation = self.evaluation_repository.update(
                db=self.db, obj_in=obj_in, db_obj=evaluation
            )
            return schemas.EvaluationOut.model_validate(update_evaluation)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while creating evaluation: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_evaluation(self, _id: int) -> Union[schemas.EvaluationOut, JSONResponse]:
        """Delete evaluation record."""
        try:
            evaluation_update = self.evaluation_repository.delete(db=self.db, _id=_id)

            return schemas.EvaluationOut.model_validate(evaluation_update)

        except (DatabaseException, APIException) as e:
            logger.error(
                f"Database error occurred while deleting evaluation: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
