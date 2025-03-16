"""Question Result Repository."""
from typing import List, cast

from sqlalchemy.orm import Session

from app.models import QuestionResult
from app.repositories.base import BaseRepository
from app.schemas import QuestionResultIn, QuestionResultUpdate


class QuestionResultRepository(
    BaseRepository[QuestionResult, QuestionResultIn, QuestionResultUpdate]
):
    """Question Result Repository Class."""

    @staticmethod
    def get_all_by_evaluation_result_id(
            db: Session, *, evaluation_result_id: int
    ) -> List[QuestionResult]:
        """Get by evaluation_result_id."""
        response = cast(
            List[QuestionResult],
            db.query(QuestionResult)
            .filter(QuestionResult.evaluation_result_id == evaluation_result_id)
            .all(),
        )

        return response
