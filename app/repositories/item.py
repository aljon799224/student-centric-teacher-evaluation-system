"""Item Repository."""

from app.models.item import Item
from app.repositories.base import BaseRepository
from app.schemas.item import ItemIn


class ItemRepository(BaseRepository[Item, ItemIn, ItemIn]):
    """Item Repository Class."""

    pass
