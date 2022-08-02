import fastapi
import pytest
from starlette.testclient import TestClient
from app.app import app


@pytest.fixture(scope='session')
def client():
    yield TestClient(app)