"""User model."""

from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """User Class."""

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    disabled = Column(Boolean, nullable=True)
    hashed_password = Column(String, nullable=True)
    role = Column(String, nullable=True)
    temp_pwd = Column(Boolean, default=False)
    admin_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    evaluations = relationship("Evaluation", back_populates="user")
    question = relationship("Question", back_populates="user")
