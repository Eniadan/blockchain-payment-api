from sqlalchemy.orm import DeclarativeBase


# Base class is used by all SQLAlchemy models in the application.
# While SQLAlchemy uses this class to keep track of our database table definitions.
class Base(DeclarativeBase):
    pass