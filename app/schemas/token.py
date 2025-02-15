"""Token Schema."""

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Token Class."""

    access_token: str
    token_type: str
    name: str
    user_id: int
    temp_pwd: bool
    role: str


class TokenPayload(BaseModel):
    """Token Payload Class."""

    subject: Optional[int] = None
