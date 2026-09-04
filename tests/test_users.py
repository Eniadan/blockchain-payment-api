# TestClient allows us to test our FastAPI endpoints
# without manually starting the server or sending requests through Swagger.
from fastapi.testclient import TestClient

from app.main import app
# We then create a test client using our FastAPI application.
client = TestClient(app)
# Test that a user can be successfully registered
# when valid registration data is provided.
def test_create_user():
    response = client.post(
        "/users/",
        json={
            "email": "pytest@example.com",
            "password": "MySecret1234",
            "full_name": "Pytest User",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "pytest@example.com"
    assert data["full_name"] == "Pytest User"
    assert "password" not in data
    assert "password_hash" not in data
# Test that the API rejects registration when
# the email address is already registered.
def test_create_user_duplicate_email():
    response = client.post(
        "/users/",
        json={
            "email": "pytest@example.com",
            "password": "MySecret1234",
            "full_name": "Another User",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "User with this email already exists"