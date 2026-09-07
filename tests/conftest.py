# SQLAlchemy utilities used to create and manage our test database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
import pytest
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
# Each test can use these sessions to interact with test.db
# instead of the development database.
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)

# Create all tables defined in the application's SQLAlchemy models
# inside the test database before the tests interact with it.
Base.metadata.create_all(bind=test_engine)

# Create a database session for a test request.
# This session uses test.db instead of the application's development database.
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

# Replace the application's database dependency with our test database
# so API requests made during testing never use blockchain.db.
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def test_db():
    # Remove the existing test tables so each test starts
    # with a clean and predictable database state.
    Base.metadata.drop_all(bind=test_engine)

    # Recreate the tables required by the application models
    # before the test begins.
    Base.metadata.create_all(bind=test_engine)

    # Create a fresh database session connected to test.db.
    db = TestingSessionLocal()

    try:
        # Provide the database session to the test.
        yield db
    finally:
        # Close the session after the test finishes,
        # even if the test fails.
        db.close()