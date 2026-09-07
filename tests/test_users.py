# TestClient allows us to test our FastAPI endpoints
# without manually starting the server or sending requests through Swagger.
from fastapi.testclient import TestClient

from app.main import app


# Create a test client using our FastAPI application.
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

    # A successful user registration should return HTTP 201.
    assert response.status_code == 201

    data = response.json()

    # Verify that the API returned the correct user information.
    assert data["email"] == "pytest@example.com"
    assert data["full_name"] == "Pytest User"

    # Sensitive password information must never be returned
    # in the API response.
    assert "password" not in data
    assert "password_hash" not in data


# Test that the API rejects registration when
# the email address is already registered.
def test_create_user_duplicate_email():
    # Create the first user so the email exists in the test database.
    client.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "password": "MySecret1234",
            "full_name": "First User",
        },
    )

    # Attempt to register another user with the same email address.
    response = client.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "password": "AnotherSecret123",
            "full_name": "Second User",
        },
    )

    # The API should reject the second registration because
    # the email address is already registered.
    assert response.status_code == 409

    # Verify that the API returns the expected error message.
    assert response.json()["detail"] == "User with this email already exists"