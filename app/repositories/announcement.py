"""Announcement Repository."""

from app.models.announcement import Announcement
from app.repositories.base import BaseRepository
from app.schemas.announcement import AnnouncementIn


class AnnouncementRepository(
    BaseRepository[Announcement, AnnouncementIn, AnnouncementIn]
):
    """Announcement Repository Class."""

    pass
