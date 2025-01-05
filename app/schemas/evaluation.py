"""Evaluation Schema."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EvaluationBase(BaseModel):
    """Evaluation Base Class."""

    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    teacher_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class EvaluationUpdate(EvaluationBase):
    """Evaluation Update Class."""

    pass


class EvaluationIn(EvaluationBase):
    """Evaluation In Class."""

    pass


class EvaluationOut(EvaluationBase):
    """Evaluation Out Class."""

    id: int
