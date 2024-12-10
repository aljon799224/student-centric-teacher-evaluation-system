"""Base."""

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa: F401 # pragma: no cover
from app.models.item import Item  # noqa: F401 # pragma: no cover
from app.models.user import User  # noqa: F401 # pragma: no cover
