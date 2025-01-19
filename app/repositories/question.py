"""Question Repository."""

from app.models import Question
from app.repositories.base import BaseRepository
from app.schemas import QuestionIn, QuestionUpdate


class QuestionRepository(BaseRepository[Question, QuestionIn, QuestionUpdate]):
    """Question Repository Class."""

    pass
