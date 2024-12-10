"""Config."""

import os
import secrets

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Settings Class."""

    API_PREFIX = "/api/v1"
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    TOKEN_URL = API_PREFIX + "/auth/login/token"
    ALGORITHM = "HS256"


settings = Settings()
