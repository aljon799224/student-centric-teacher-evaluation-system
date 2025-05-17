"""Evaluation Schema."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EvaluationBase(BaseModel):
    """Evaluation Base Class."""

    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    teacher_id: int | None = None
    admin_id: int | None = None
    is_submitted: bool | None = None
    is_disabled: bool | None = False
    category: str | None = None
    comment: str | None = None
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


class EvaluationDetailedOut(EvaluationBase):
    """Evaluation Detailed Out Class."""

    id: int
    teacher_name: str | None = None


class EvaluationsOut(EvaluationBase):
    """Evaluation Out Class."""

    id: int
    teacher_name: str | None = None
