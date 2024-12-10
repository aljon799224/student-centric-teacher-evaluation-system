"""Item Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import Item
from app.repositories.item import ItemRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


class ItemUseCase:
    """Item Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db and Item Repository."""
        self.db = db
        self.item_repository = ItemRepository(Item)

    def get_items(self) -> Union[Page[schemas.ItemOut], JSONResponse]:
        """Get all items record."""
        try:
            items = self.item_repository.get_all(self.db)

        except DatabaseException as e:
            logger.error(f"Database error occurred while fetching items: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(items)

    def get_item(self, _id: int) -> Union[schemas.ItemOut, JSONResponse]:
        """Get item record."""
        try:
            item = self.item_repository.get(self.db, _id)

            return schemas.ItemOut.model_validate(item)

        except APIException as e:
            logger.error(f"Database error occurred while fetching item: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def create_item(
        self,
        *,
        obj_in: schemas.ItemIn,
    ) -> Union[schemas.ItemOut, JSONResponse]:  # schemas.ItemOut
        """Create item record."""
        try:
            item = self.item_repository.create(db=self.db, obj_in=obj_in)

            return schemas.ItemOut.model_validate(item)

        except DatabaseException as e:
            logger.error(f"Database error occurred while creating item: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_item(
        self,
        _id: int,
        *,
        obj_in: schemas.ItemIn,
    ) -> Union[schemas.ItemOut, JSONResponse]:
        """Update item record."""
        try:
            item = self.item_repository.get(db=self.db, _id=_id)

            item_update = self.item_repository.update(
                db=self.db, obj_in=obj_in, db_obj=item
            )

            return schemas.ItemOut.model_validate(item_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while updating item: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_item(self, _id: int) -> Union[schemas.ItemOut, JSONResponse]:
        """Delete item record."""
        try:
            item_update = self.item_repository.delete(db=self.db, _id=_id)

            return schemas.ItemOut.model_validate(item_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while deleting item: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
