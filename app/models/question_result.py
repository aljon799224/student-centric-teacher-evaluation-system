"""Question Result model."""

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class QuestionResult(Base):
    """Question Result Class."""

    __tablename__ = "question_result"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)
    student_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    evaluation_result_id = Column(
        Integer, ForeignKey("evaluation_result.id", ondelete="CASCADE"), nullable=False
    )
    student_name = Column(String, nullable=True)
    evaluation_title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="question_results")
    evaluation_result = relationship(
        "EvaluationResult", back_populates="question_results"
    )
