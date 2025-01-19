"""Question model."""

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Question(Base):
    """Question Class."""

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)
    student_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    evaluation_id = Column(
        Integer, ForeignKey("evaluation.id", ondelete="CASCADE"), nullable=False
    )
    student_name = Column(String, nullable=True)
    evaluation_title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship(
        "User", back_populates="question"
    )  # User role must be student in FE
    evaluation = relationship(
        "Evaluation", back_populates="questions", passive_deletes=True
    )
