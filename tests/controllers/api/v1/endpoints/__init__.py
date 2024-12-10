"""Endpoints unit tests."""

from starlette.testclient import TestClient

from app.main import app

test_client = TestClient(app)
