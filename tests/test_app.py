import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    assert "Signed up" in data["message"]
    
    # Clean up
    activities["Chess Club"]["participants"].remove("newstudent@mergington.edu")


def test_signup_duplicate_student(client):
    """Test that a student cannot sign up twice for the same activity"""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post(
        "/activities/Fake Club/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_from_activity(client):
    """Test unregistering a student from an activity"""
    email = "newstudent2@mergington.edu"
    # First, sign up
    activities["Programming Class"]["participants"].append(email)
    
    # Then, unregister
    response = client.delete(
        "/activities/Programming Class/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    assert email not in activities["Programming Class"]["participants"]
    assert "Unregistered" in response.json()["message"]


def test_unregister_nonexistent_activity(client):
    """Test unregistering from a non-existent activity"""
    response = client.delete(
        "/activities/Fake Club/unregister",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_registered_student(client):
    """Test unregistering a student who is not registered"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
