"""Item Schemas."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    """Item Class."""

    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None


class ItemIn(ItemBase):
    """ItemIn Class."""

    pass


class ItemOut(ItemBase):
    """ItemOut Class."""

    id: int
