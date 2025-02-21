"""Evaluation Result Schema."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EvaluationResultBase(BaseModel):
    """Evaluation Base Class."""

    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    teacher_id: int | None = None
    evaluation_id: int | None = None
    admin_id: int | None = None
    is_submitted: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class EvaluationResultUpdate(EvaluationResultBase):
    """Evaluation Result Update Class."""

    pass


class EvaluationResultIn(EvaluationResultBase):
    """Evaluation Result In Class."""

    pass


class EvaluationResultOut(EvaluationResultBase):
    """Evaluation Result Out Class."""

    id: int


class EvaluationDetailedResultOut(EvaluationResultBase):
    """Evaluation Result Detailed Out Class."""

    id: int
    teacher_name: str | None = None
    student_name: str | None = None


class EvaluationsResultOut(EvaluationResultBase):
    """Evaluation Result Out Class."""

    id: int
    teacher_name: str | None = None
    student_name: str | None = None
