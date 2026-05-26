from uuid import UUID

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.models import Base, Photo, Trip


@pytest.fixture
def session():
    engine = create_engine("sqlite+pysqlite:///:memory:")

    # Turn on foreign keys for SQLite for dev.
    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys = ON")

    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


# Filler data for creating instances.


def get_test_user() -> dict:
    return {"email": "example@gmail.com", "first_name": "Sal", "last_name": "Vulcano"}


def get_test_photo(author_id: UUID, trip_id: UUID | None = None) -> Photo:
    return {
        "author_id": author_id,
        "trip_id": trip_id,
        "title": "Title",
        "url": "www.exampleurl.com",
    }


def get_test_trip(author_id: UUID) -> Trip:
    return {
        "author_id": author_id,
        "title": "Title",
    }
