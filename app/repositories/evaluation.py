"""Evaluation Repository."""

from app.models import Evaluation
from app.repositories.base import BaseRepository
from app.schemas import EvaluationUpdate, EvaluationIn


class EvaluationRepository(BaseRepository[Evaluation, EvaluationIn, EvaluationUpdate]):
    """Evaluation Repository Class."""

    pass
