"""Question Result Schema."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QuestionResultBase(BaseModel):
    """Question Result Base Class."""

    model_config = ConfigDict(from_attributes=True)

    question_text: str | None = None
    rating: int | None = None
    comment: str | None = None
    student_id: int | None = None
    evaluation_result_id: int | None = None
    student_name: str | None = None
    evaluation_title: str | None = None
    category: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class QuestionResultIn(QuestionResultBase):
    """Question Result Update Class."""

    pass


class QuestionResultUpdate(QuestionResultBase):
    """Question Result In Class."""

    pass


class QuestionResultOut(QuestionResultBase):
    """Question Result Out Class."""

    id: int
