"""Item model."""

from sqlalchemy import Column, String, Integer

from app.db.base_class import Base


class Item(Base):
    """Item Class."""

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
