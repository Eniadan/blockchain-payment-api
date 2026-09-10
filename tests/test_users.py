# Pytest provides the test runner and utilities such as pytest.raises().
import pytest

# MagicMock allows us to simulate database behavior
# without intentionally breaking the real test database.
from unittest.mock import MagicMock

# TestClient allows us to test our FastAPI endpoints
# without manually starting the server or sending requests through Swagger.
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user import UserCreate
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

# Test that the API rejects a registration request
# when the email address is not in a valid email format.
def test_create_user_invalid_email():
    response = client.post(
        "/users/",
        json={
            "email": "not-an-email",
            "password": "MySecret1234",
            "full_name": "Invalid Email User",
        },
    )

    # FastAPI should return HTTP 422 when request validation fails.
    assert response.status_code == 422

# Test that the API rejects a registration request
# when the required email field is completely missing.
def test_create_user_missing_email():
    response = client.post(
        "/users/",
        json={
            "password": "MySecret1234",
            "full_name": "Missing Email User",
        },
    )

    # FastAPI should return HTTP 422 when a required field is missing.
    assert response.status_code == 422

    # Test that a user's password is hashed before it is stored
# in the database and that the original password is never stored.
def test_password_is_hashed():
    client.post(
        "/users/",
        json={
            "email": "hash@example.com",
            "password": "MySecret1234",
            "full_name": "Hash Test User",
        },
    )

    # Import the User model so we can inspect the database record
    # directly during this security-focused test.
    from app.models.user import User
    from tests.conftest import TestingSessionLocal

    db = TestingSessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == "hash@example.com")
            .first()
        )

        # A user should have been created successfully.
        assert user is not None

        # A password hash must exist in the database.
        assert user.password_hash

        # The original plain-text password must never be stored.
        assert user.password_hash != "MySecret1234"

    finally:
        # Always close the database session after inspecting the record.
        db.close()

# Test that an existing user can be retrieved using their database ID.
def test_get_user():
    create_response = client.post(
        "/users/",
        json={
            "email": "getuser@example.com",
            "password": "MySecret1234",
            "full_name": "Get User Test",
        },
    )

    # Confirm that the user was created successfully before
    # attempting to retrieve them.
    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    # Request the newly created user using their database ID.
    response = client.get(f"/users/{user_id}")

    # An existing user should be returned successfully.
    assert response.status_code == 200

    data = response.json()

    # Verify that the returned user is the one we created.
    assert data["id"] == user_id
    assert data["email"] == "getuser@example.com"
    assert data["full_name"] == "Get User Test"

    # Sensitive password information must never be exposed.
    assert "password" not in data
    assert "password_hash" not in data

# Test that the API returns a 404 error when a user
# with the requested ID does not exist.
def test_get_user_not_found():
    response = client.get("/users/99999")

    # The API should return HTTP 404 when the user cannot be found.
    assert response.status_code == 404

    # Verify that the API returns the expected error message.
    assert response.json()["detail"] == "User not found"

# Test that the API rejects a registration request
# when the required password field is missing.
def test_create_user_missing_password():
    response = client.post(
        "/users/",
        json={
            "email": "missingpassword@example.com",
            "full_name": "Missing Password User",
        },
    )

    # FastAPI should return HTTP 422 when a required field is missing.
    assert response.status_code == 422

    # Test that the API rejects a registration request
# when the required full_name field is missing.
def test_create_user_missing_full_name():
    response = client.post(
        "/users/",
        json={
            "email": "missingname@example.com",
            "password": "MySecret1234",
        },
    )

    # FastAPI should return HTTP 422 when a required field is missing.
    assert response.status_code == 422

    # Test that a database failure during user creation
# causes the transaction to be rolled back.
def test_create_user_rolls_back_on_database_error():
    from app.services.user_service import create_user

    # Create a fake database session so we can control
    # database behavior without changing our real test database.
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    # Simulate a database failure when commit() is called.
    db.commit.side_effect = Exception("Database error")

    user_data = UserCreate(
        email="rollback@example.com",
        password="MySecret1234",
        full_name="Rollback Test User",
    )

    # The service should re-raise the database error after
    # rolling back the failed transaction.
    with pytest.raises(Exception, match="Database error"):
        create_user(db, user_data)

    # Verify that rollback() was called after the database failure.
    db.rollback.assert_called_once()

