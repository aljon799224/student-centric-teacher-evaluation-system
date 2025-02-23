"""Evaluation model."""

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class EvaluationResult(Base):
    """Evaluation Result Class."""

    __tablename__ = "evaluation_result"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    teacher_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    evaluation_id = Column(
        Integer, ForeignKey("evaluation.id", ondelete="CASCADE"), nullable=True
    )
    admin_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_submitted = Column(Boolean, nullable=True)

    user = relationship(
        "User", back_populates="evaluation_results"
    )  # User role must be teacher in FE
    evaluation = relationship("Evaluation", back_populates="evaluation_results")
