"""Base Repository."""

import logging
from http import HTTPStatus
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.db.base_class import Base
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base Repository."""

    def __init__(self, model: Type[ModelType]):
        """Repository object with default methods to CRUD.

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get_all(self, db: Session) -> List[ModelType]:
        """Retrieve all records, with optional pagination."""
        try:
            return db.query(self.model).all()
        except Exception as e:
            # Log the exception (you may want to use your logger here)
            logger.error(f"Error fetching all items: {str(e)}")
            raise DatabaseException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching the items.",
            ) from e

    def get(self, db: Session, _id: int) -> Optional[ModelType]:
        """Get record by its ID.."""
        item = db.query(self.model).filter(self.model.id == _id).first()

        if item is None:
            raise APIException(
                status_code=HTTPStatus.NOT_FOUND, detail="Record not found."
            )
        return item

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create record."""
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except exc.IntegrityError as e:
            error = e.orig.args

            raise DatabaseException(
                status_code=HTTPStatus.CONFLICT, detail=error[0]
            ) from e

        except Exception as e:
            raise DatabaseException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            ) from e

        return db_obj

    @staticmethod
    def update(
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update record by its ID."""
        try:
            obj_data = jsonable_encoder(db_obj)
            update_data = (
                obj_in.model_dump(exclude_unset=True)
                if not isinstance(obj_in, dict)
                else obj_in
            )

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        except exc.IntegrityError as e:
            error = e.orig.args
            raise DatabaseException(
                status_code=HTTPStatus.CONFLICT, detail=error[0]
            ) from e

        except Exception as e:
            # Handle unexpected exceptions and raise a DatabaseException
            raise DatabaseException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during the update.",
            ) from e

        return db_obj

    def delete(self, db: Session, *, _id: int) -> ModelType:
        """Delete a record by its ID."""
        try:
            obj = db.query(self.model).get(_id)

            if obj is None:
                raise APIException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="Record not found.",
                )

            db.delete(obj)
            db.commit()
            return obj

        except APIException as e:
            # Re-raise the APIException to propagate it correctly
            raise e

        except Exception as e:
            raise DatabaseException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during the deletion.",
            ) from e
