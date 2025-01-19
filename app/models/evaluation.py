"""Evaluation model."""

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Evaluation(Base):
    """Evaluation Class."""

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    teacher_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    admin_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship(
        "User", back_populates="evaluations"
    )  # User role must be teacher in FE
    questions = relationship(
        "Question", back_populates="evaluation", cascade="all, delete-orphan"
    )
