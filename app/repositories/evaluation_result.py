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
    def get_all_by_evaluation_id(
        db: Session, *, evaluation_id: int
    ) -> List[EvaluationResult]:
        """Get by evaluation_id."""
        response = cast(
            List[EvaluationResult],
            db.query(EvaluationResult)
            .filter(EvaluationResult.evaluation_id == evaluation_id)
            .all(),
        )

        return response


    @staticmethod
    def get_all_by_teacher_id(
        db: Session, *, teacher_id: int
    ) -> List[EvaluationResult]:
        """Get by teacher_id."""
        response = cast(
            List[EvaluationResult],
            db.query(EvaluationResult)
            .filter(EvaluationResult.teacher_id == teacher_id)
            .all(),
        )

        return response
