from uuid import UUID

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, User, Photo, Trip


@pytest.fixture
def session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


# Filler data for creating instances.


def get_test_user() -> dict:
    return {"email": "example@gmail.com", "first_name": "Sal", "last_name": "Vulcano"}


def get_test_photo(author_id: UUID) -> Photo:
    return {
        "author_id": author_id,
        "title": "Title",
        "url": "www.exampleurl.com",
    }


def get_test_trip(author_id: UUID) -> Trip:
    return {
        "author_id": author_id,
        "title": "Title",
    }
