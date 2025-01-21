"""Msg."""

from pydantic import BaseModel


class Msg(BaseModel):
    """Msg Class."""

    message: str
