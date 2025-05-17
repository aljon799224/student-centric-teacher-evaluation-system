"""Question Schema."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    """Question Base Class."""

    model_config = ConfigDict(from_attributes=True)

    question_text: str | None = None
    rating: int | None = None
    comment: str | None = None
    category: str | None = None
    student_id: int | None = None
    evaluation_id: int | None = None
    student_name: str | None = None
    evaluation_title: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class QuestionIn(QuestionBase):
    """Question Update Class."""

    pass


class QuestionUpdate(QuestionBase):
    """Question In Class."""

    pass


class QuestionOut(QuestionBase):
    """Question Out Class."""

    id: int
