"""Announcement Schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnnouncementBase(BaseModel):
    """Announcement Class."""

    model_config = ConfigDict(from_attributes=True)

    announcement_text: Optional[str] = None
    admin_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AnnouncementIn(AnnouncementBase):
    """IteAnnouncementInmIn Class."""

    pass


class AnnouncementOut(AnnouncementBase):
    """AnnouncementOut Class."""

    id: int


class AnnouncementsOut(AnnouncementBase):
    """AnnouncementOut Class."""

    id: int
    name: str
    role: str
