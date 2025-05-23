"""Evaluation model."""

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Evaluation(Base):
    """Evaluation Class."""

    __tablename__ = "evaluation"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    teacher_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    admin_id = Column(Integer, nullable=True)
    category = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_submitted = Column(Boolean, nullable=True)
    is_disabled = Column(Boolean, nullable=True)

    user = relationship("User", back_populates="evaluations")
    questions = relationship(
        "Question", back_populates="evaluation", cascade="all, delete-orphan"
    )
    evaluation_results = relationship(
        "EvaluationResult", back_populates="evaluation", cascade="all, delete-orphan"
    )
