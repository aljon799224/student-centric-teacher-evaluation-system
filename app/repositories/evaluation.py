"""Evaluation Repository."""

from typing import List, cast

from sqlalchemy.orm import Session

from app.models import Evaluation
from app.repositories.base import BaseRepository
from app.schemas import EvaluationUpdate, EvaluationIn


class EvaluationRepository(BaseRepository[Evaluation, EvaluationIn, EvaluationUpdate]):
    """Evaluation Repository Class."""

    @staticmethod
    def get_all_by_teacher_id(db: Session, *, teacher_id: int) -> List[Evaluation]:
        """Get by teacher_id."""
        response = cast(
            List[Evaluation],
            db.query(Evaluation).filter(Evaluation.teacher_id == teacher_id).all(),
        )
        print(response)
        print(response)
        return response
