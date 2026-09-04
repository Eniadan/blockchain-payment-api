from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# Create the SQLAlchemy engine using the database URL
# defined in the application's configuration.
# The engine manages the connection between our application and the database.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# Create a session factory that will be used to create
# individual database sessions for our application.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Provide a database session to FastAPI routes through dependency injection.
# The session is automatically closed after the request is finished,
# even if an error occurs while processing the request.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()