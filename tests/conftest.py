import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture for FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """Fixture for a sample activity name"""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Fixture for a sample email"""
    return "newstudent@mergington.edu"
