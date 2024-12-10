"""Main."""

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from app.controllers.api.v1.endpoints.base import api_controller
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(title="Project", version="1")

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_controller(app)
add_pagination(app)
