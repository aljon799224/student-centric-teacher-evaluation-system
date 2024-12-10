"""Base Class."""

from typing import Any

from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base Class."""

    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        """Return the table name based on class name in lowercase."""
        return cls.__name__.lower()
