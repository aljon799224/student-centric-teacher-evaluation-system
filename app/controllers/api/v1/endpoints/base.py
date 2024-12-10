"""Base Endpoint."""

from app.controllers.api.v1.endpoints.auth import auth_router
from app.controllers.api.v1.endpoints.item import item_router
from app.controllers.api.v1.endpoints.user import user_router
from app.core.config import settings


def api_controller(app):
    """API Controller."""
    app.include_router(item_router, prefix=f"{settings.API_PREFIX}", tags=["Item"])
    app.include_router(user_router, prefix=f"{settings.API_PREFIX}", tags=["User"])
    app.include_router(auth_router, prefix=f"{settings.API_PREFIX}", tags=["Login"])
