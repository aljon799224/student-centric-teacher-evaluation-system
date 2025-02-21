"""Announcement Endpoint."""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.announcement import AnnouncementUseCase

announcement_router = APIRouter()


@announcement_router.get("/announcement", response_model=Page[schemas.AnnouncementsOut])
def get_announcements(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all announcements."""
    announcement_uc = AnnouncementUseCase(db=db)

    announcements = announcement_uc.get_announcements()

    return announcements


@announcement_router.get("/announcement/{_id}", response_model=schemas.AnnouncementOut)
def get_announcement(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get announcement by ID."""
    announcement_uc = AnnouncementUseCase(db=db)

    announcement = announcement_uc.get_announcement(_id=_id)

    return announcement


@announcement_router.post("/announcement", response_model=schemas.AnnouncementOut)
def create(
    obj_in: schemas.AnnouncementIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Create announcement."""
    announcement_uc = AnnouncementUseCase(db=db)

    announcement = announcement_uc.create_announcement(obj_in=obj_in)

    return announcement


@announcement_router.put("/announcement/{_id}", response_model=schemas.AnnouncementOut)
def update(
    _id: int,
    obj_in: schemas.AnnouncementIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Update announcement by ID."""
    announcement_uc = AnnouncementUseCase(db=db)

    announcement = announcement_uc.update_announcement(obj_in=obj_in, _id=_id)

    return announcement


@announcement_router.delete(
    "/announcement/{_id}", response_model=schemas.AnnouncementOut
)
def delete(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Delete announcement by ID."""
    announcement_uc = AnnouncementUseCase(db=db)

    announcement = announcement_uc.delete_announcement(_id=_id)

    return announcement
