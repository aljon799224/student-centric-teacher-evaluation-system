"""Base Endpoint."""

from app.controllers.api.v1.endpoints.auth import auth_router
from app.controllers.api.v1.endpoints.evaluation import evaluation_router
from app.controllers.api.v1.endpoints.item import item_router
from app.controllers.api.v1.endpoints.question import question_router
from app.controllers.api.v1.endpoints.user import user_router
from app.controllers.api.v1.endpoints.announcement import announcement_router
from app.controllers.api.v1.endpoints.evaluation_results import evaluation_result_router
from app.controllers.api.v1.endpoints.question_result import question_result_router
from app.core.config import settings


def api_controller(app):
    """API Controller."""
    app.include_router(item_router, prefix=f"{settings.API_PREFIX}", tags=["Item"])
    app.include_router(user_router, prefix=f"{settings.API_PREFIX}", tags=["User"])
    app.include_router(
        evaluation_router, prefix=f"{settings.API_PREFIX}", tags=["Evaluation"]
    )
    app.include_router(
        question_router, prefix=f"{settings.API_PREFIX}", tags=["Question"]
    )
    app.include_router(
        announcement_router, prefix=f"{settings.API_PREFIX}", tags=["Announcement"]
    )
    app.include_router(
        evaluation_result_router,
        prefix=f"{settings.API_PREFIX}",
        tags=["Evaluation Result"],
    )
    app.include_router(
        question_result_router,
        prefix=f"{settings.API_PREFIX}",
        tags=["Question Result"],
    )
    app.include_router(auth_router, prefix=f"{settings.API_PREFIX}", tags=["Login"])
