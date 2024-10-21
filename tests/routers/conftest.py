import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def app() -> FastAPI:
    app = create_app()

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
