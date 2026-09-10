# SQLAlchemy utilities used to create and manage our test database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

# Import the application's database dependency so we can replace it
# with our test database during automated tests.
from app.db.session import get_db

# Import the SQLAlchemy Base so we can create the same database
# tables defined by our application models inside the test database.
from app.db.base import Base

# Import the User model so SQLAlchemy registers the users table
# in Base.metadata before the test database tables are created.
from app.models.user import User

# Import the FastAPI application so our tests use the real application.
from app.main import app


# Use a separate SQLite database for automated tests so that
# tests never modify the application's development database.
TEST_DATABASE_URL = "sqlite:///./test.db"


# Create a SQLAlchemy engine specifically for the test database.
# check_same_thread=False allows the SQLite database to be used
# safely with FastAPI's TestClient during testing.
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Create a session factory for the test database.
# FastAPI will use this factory when our database dependency
# is overridden during automated tests.
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


# Create a database session for API requests during tests.
# This replaces the application's normal database dependency,
# ensuring API tests use test.db instead of blockchain.db.
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# Replace the application's database dependency with our test database.
# This means requests made through TestClient will use test.db.
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def test_db():
    # Remove existing test tables so every test starts
    # with a clean and predictable database state.
    Base.metadata.drop_all(bind=test_engine)

    # Recreate the tables required by the application's models
    # before the test begins.
    Base.metadata.create_all(bind=test_engine)

    # The fixture does not need to create a separate session here.
    # API requests receive their own session through override_get_db().
    yield