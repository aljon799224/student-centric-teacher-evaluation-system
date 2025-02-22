"""Evaluation Result Repository."""

from typing import List, cast

from sqlalchemy.orm import Session

from app.models import EvaluationResult
from app.repositories.base import BaseRepository
from app.schemas import EvaluationResultUpdate, EvaluationResultIn


class EvaluationResultRepository(
    BaseRepository[EvaluationResult, EvaluationResultIn, EvaluationResultUpdate]
):
    """Evaluation Result Repository Class."""

    @staticmethod
    def get_all_by_evaluation_and_admin_id(
        db: Session, *, evaluation_id: int, admin_id: int
    ) -> List["EvaluationResult"]:
        """Get evaluation results filtered by both evaluation_id and admin_id."""
        response = cast(
            List[EvaluationResult],
            db.query(EvaluationResult)
            .filter(
                EvaluationResult.evaluation_id == evaluation_id,
                EvaluationResult.admin_id == admin_id,  # AND condition
            )
            .all(),
        )

        return response

    @staticmethod
    def get_all_by_student_id(
        db: Session, *, student_id: int
    ) -> List[EvaluationResult]:
        """Get by teacher_id."""
        response = cast(
            List[EvaluationResult],
            db.query(EvaluationResult)
            .filter(EvaluationResult.admin_id == student_id)
            .all(),
        )

        return response
