"""Evaluation Result Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import EvaluationResult, User, QuestionResult
from app.repositories.evaluation_result import EvaluationResultRepository
from app.repositories.question_result import QuestionResultRepository
from app.repositories.user import UserRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


class EvaluationResultUseCase:
    """Evaluation Result Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db."""
        self.db = db
        self.evaluation_result_repository = EvaluationResultRepository(EvaluationResult)
        self.question_result_repository = QuestionResultRepository(QuestionResult)
        self.user_repository = UserRepository(User)

    def get_evaluation_results(
        self,
    ) -> Union[Page[schemas.EvaluationsResultOut], JSONResponse]:
        """Get all evaluations results record."""
        try:
            response = []

            evaluation_results = self.evaluation_result_repository.get_all(self.db)

            for evaluation in evaluation_results:
                user = self.user_repository.get(self.db, evaluation.teacher_id)
                user_student = self.user_repository.get(self.db, evaluation.admin_id)

                evaluation_dict = {
                    key: value
                    for key, value in vars(evaluation).items()
                    if not key.startswith("_")
                }

                full_name = f"{user.first_name} {user.middle_name} {user.last_name}"
                full_name_student = (
                    f"{user_student.first_name} "
                    f"{user_student.middle_name} "
                    f"{user_student.last_name}"
                )
                evaluation_dict.update(
                    {"teacher_name": full_name, "student_name": full_name_student}
                )

                response.append(evaluation_dict)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching evaluation results: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(response)

    def get_evaluation_results_by_evaluation_and_admin_id(
        self, evaluation_id: int, admin_id: int
    ) -> Union[Page[schemas.EvaluationResultOut], JSONResponse]:
        """Get all evaluations record by evaluation and admin id."""
        try:
            response = []

            evaluation_results = (
                self.evaluation_result_repository.get_all_by_evaluation_and_admin_id(
                    self.db, evaluation_id=evaluation_id, admin_id=admin_id
                )
            )

            for evaluation in evaluation_results:
                user = self.user_repository.get(self.db, evaluation.teacher_id)
                user_student = self.user_repository.get(self.db, evaluation.admin_id)

                evaluation_dict = {
                    key: value
                    for key, value in vars(evaluation).items()
                    if not key.startswith("_")
                }

                full_name = f"{user.first_name} {user.middle_name} {user.last_name}"
                full_name_student = (
                    f"{user_student.first_name} "
                    f"{user_student.middle_name} "
                    f"{user_student.last_name}"
                )
                evaluation_dict.update(
                    {"teacher_name": full_name, "student_name": full_name_student}
                )

                response.append(evaluation_dict)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching evaluations: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(response)

    def get_evaluation_results_by_evaluation_id(
        self, evaluation_id: int
    ) -> Union[Page[schemas.EvaluationDetailedResultOut], JSONResponse]:
        """Get all evaluations record by evaluation id."""
        try:
            response = []

            evaluation_results = (
                self.evaluation_result_repository.get_all_by_evaluation_id(
                    self.db, evaluation_id=evaluation_id
                )
            )

            for evaluation in evaluation_results:
                user = self.user_repository.get(self.db, evaluation.teacher_id)
                user_student = self.user_repository.get(self.db, evaluation.admin_id)

                evaluation_dict = {
                    key: value
                    for key, value in vars(evaluation).items()
                    if not key.startswith("_")
                }

                full_name = f"{user.first_name} {user.middle_name} {user.last_name}"
                full_name_student = (
                    f"{user_student.first_name} "
                    f"{user_student.middle_name} "
                    f"{user_student.last_name}"
                )
                evaluation_dict.update(
                    {"teacher_name": full_name, "student_name": full_name_student}
                )

                response.append(evaluation_dict)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching evaluations: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(response)



    def get_evaluation_results_by_teacher_id(
        self, teacher_id: int
    ) -> Union[Page[schemas.EvaluationDetailedResultOut], JSONResponse]:
        """Get all evaluations record by evaluation id."""
        try:
            response = []

            evaluation_results = (
                self.evaluation_result_repository.get_all_by_teacher_id(
                    self.db, teacher_id=teacher_id
                )
            )

            for evaluation in evaluation_results:
                user = self.user_repository.get(self.db, evaluation.teacher_id)
                user_student = self.user_repository.get(self.db, evaluation.admin_id)
                question_results = self.question_result_repository.get_all_by_evaluation_result_id(
                    self.db, evaluation_result_id=evaluation.id
                )


                ratings_1 = [qr.rating for qr in question_results if qr.category == 'Personal & Professional Characteristics']
                ratings_2 = [qr.rating for qr in question_results if qr.category == 'Classroom Teaching']
                ratings_3 = [qr.rating for qr in question_results if qr.category == 'Classroom Management and Control']
                ratings_4 = [qr.rating for qr in question_results if qr.category == 'Lesson Plans']
                average_rating_1 = round(sum(ratings_1) / len(ratings_1), 2) if ratings_1 else 0
                average_rating_2 = round(sum(ratings_2) / len(ratings_2), 2) if ratings_2 else 0
                average_rating_3 = round(sum(ratings_3) / len(ratings_3), 2) if ratings_3 else 0
                average_rating_4 = round(sum(ratings_4) / len(ratings_4), 2) if ratings_4 else 0
                average_rating = round((average_rating_1 + average_rating_2 + average_rating_3 + average_rating_4) / 4, 2)




                evaluation_dict = {
                    key: value
                    for key, value in vars(evaluation).items()
                    if not key.startswith("_")
                }

                full_name = f"{user.first_name} {user.middle_name} {user.last_name}"
                full_name_student = (
                    f"{user_student.first_name} "
                    f"{user_student.middle_name} "
                    f"{user_student.last_name}"
                )
                evaluation_dict.update(
                    {
                        "teacher_name": full_name,
                        "student_name": full_name_student,
                        "average_1": average_rating_1,
                        "average_2": average_rating_2,
                        "average_3": average_rating_3,
                        "average_4": average_rating_4,
                        "average": average_rating,
                        "comment": evaluation.comment
                    }
                )

                response.append(evaluation_dict)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching evaluations: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(response)


    def get_evaluation_result(
        self, _id: int
    ) -> Union[schemas.EvaluationResultOut, JSONResponse]:
        """Get evaluation record."""
        try:
            evaluation_result = self.evaluation_result_repository.get(self.db, _id)

            return schemas.EvaluationResultOut.model_validate(evaluation_result)

        except APIException as e:
            logger.error(
                f"Database error occurred while fetching evaluation result: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def create_evaluation_result(
        self,
        *,
        obj_in: schemas.EvaluationResultIn,
    ) -> Union[schemas.EvaluationDetailedResultOut, JSONResponse]:
        """Create evaluation result record."""
        try:
            evaluation_result = self.evaluation_result_repository.create(
                db=self.db, obj_in=obj_in
            )
            user = self.user_repository.get(self.db, evaluation_result.teacher_id)
            evaluation_result_dict = (
                evaluation_result.__dict__.copy()
            )  # Create a copy of the dictionary
            evaluation_result_dict.pop("_sa_instance_state", None)
            full_name = f"{user.first_name} {user.middle_name} {user.last_name}"
            evaluation_result_dict.update({"teacher_name": full_name})

            return schemas.EvaluationDetailedResultOut(**evaluation_result_dict)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while creating evaluation result: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_evaluation_result(
        self,
        *,
        _id: int,
        obj_in: schemas.EvaluationResultUpdate,
    ) -> Union[schemas.EvaluationDetailedResultOut, JSONResponse]:
        """Update evaluation result record."""
        try:
            evaluation = self.evaluation_result_repository.get(db=self.db, _id=_id)

            update_evaluation = self.evaluation_result_repository.update(
                db=self.db, obj_in=obj_in, db_obj=evaluation
            )

            user = self.user_repository.get(self.db, update_evaluation.teacher_id)
            evaluation_dict = (
                update_evaluation.__dict__.copy()
            )  # Create a copy of the dictionary
            evaluation_dict.pop("_sa_instance_state", None)
            full_name = f"{user.first_name} {user.middle_name} {user.last_name}"
            evaluation_dict.update({"teacher_name": full_name})

            return schemas.EvaluationDetailedResultOut(**evaluation_dict)

        except (DatabaseException, APIException) as e:
            logger.error(
                f"Database error occurred while creating evaluation result: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_evaluation(
        self, _id: int
    ) -> Union[schemas.EvaluationResultOut, JSONResponse]:
        """Delete evaluation result record."""
        try:
            evaluation_delete = self.evaluation_result_repository.delete(
                db=self.db, _id=_id
            )

            return schemas.EvaluationResultOut.model_validate(evaluation_delete)

        except (DatabaseException, APIException) as e:
            logger.error(
                f"Database error occurred while deleting evaluation result: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
