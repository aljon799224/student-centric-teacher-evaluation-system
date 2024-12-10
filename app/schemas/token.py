"""Token Schema."""

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Token Class."""

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Token Payload Class."""

    subject: Optional[int] = None
