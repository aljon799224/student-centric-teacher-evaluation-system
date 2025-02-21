"""Question Result Repository."""

from app.models import QuestionResult
from app.repositories.base import BaseRepository
from app.schemas import QuestionResultIn, QuestionResultUpdate


class QuestionResultRepository(
    BaseRepository[QuestionResult, QuestionResultIn, QuestionResultUpdate]
):
    """Question Result Repository Class."""

    pass
