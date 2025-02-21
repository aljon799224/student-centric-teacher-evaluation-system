"""Announcement Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import Announcement, User
from app.repositories.announcement import AnnouncementRepository
from app.repositories.user import UserRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


class AnnouncementUseCase:
    """Announcement Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db."""
        self.db = db
        self.announcement_repository = AnnouncementRepository(Announcement)
        self.user_repository = UserRepository(User)

    def get_announcements(self) -> Union[Page[schemas.AnnouncementsOut], JSONResponse]:
        """Get all announcements record."""
        try:
            response = []
            announcements = self.announcement_repository.get_all(self.db)

            for announcement in announcements:
                user = self.user_repository.get(self.db, announcement.admin_id)

                announcement_dict = {
                    key: value
                    for key, value in vars(announcement).items()
                    if not key.startswith("_")
                }

                full_name = f"{user.first_name} {user.middle_name} {user.last_name}"
                announcement_dict.update(
                    {"name": full_name, "role": user.role.capitalize()}
                )

                response.append(announcement_dict)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching announcements: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(response)

    def get_announcement(
        self, _id: int
    ) -> Union[schemas.AnnouncementOut, JSONResponse]:
        """Get announcement record."""
        try:
            announcement = self.announcement_repository.get(self.db, _id)

            return schemas.AnnouncementOut.model_validate(announcement)

        except APIException as e:
            logger.error(
                f"Database error occurred while fetching announcement: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def create_announcement(
        self,
        *,
        obj_in: schemas.AnnouncementIn,
    ) -> Union[schemas.AnnouncementOut, JSONResponse]:
        """Create announcement record."""
        try:
            announcement = self.announcement_repository.create(
                db=self.db, obj_in=obj_in
            )
            return schemas.AnnouncementOut.model_validate(announcement)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while creating announcement: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_announcement(
        self,
        *,
        _id: int,
        obj_in: schemas.AnnouncementIn,
    ) -> Union[schemas.AnnouncementOut, JSONResponse]:
        """Update announcement record."""
        try:
            announcement = self.announcement_repository.get(db=self.db, _id=_id)

            update_announcement = self.announcement_repository.update(
                db=self.db, obj_in=obj_in, db_obj=announcement
            )
            return schemas.AnnouncementOut.model_validate(update_announcement)

        except (DatabaseException, APIException) as e:
            logger.error(
                f"Database error occurred while creating announcement: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_announcement(
        self, _id: int
    ) -> Union[schemas.AnnouncementOut, JSONResponse]:
        """Delete announcement record."""
        try:
            announcement_update = self.announcement_repository.delete(
                db=self.db, _id=_id
            )

            return schemas.AnnouncementOut.model_validate(announcement_update)

        except (DatabaseException, APIException) as e:
            logger.error(
                f"Database error occurred while deleting announcement: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
