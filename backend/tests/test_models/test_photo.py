import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Photo, User, Trip, PhotoMetadata
from tests.conftest import get_test_user, get_test_photo, get_test_trip


def test_create_photo_no_trip(session):
    """Photos can optionally belong to a trip and only one trip"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    photo = Photo(**get_test_photo(author_id=user.id))

    session.add(photo)
    session.commit()

    fetched = session.get(Photo, photo.id)

    assert fetched is not None
    assert fetched.trip is None


def test_create_photo_with_trip(session):
    """Photos can optionally belong to a trip and only one trip"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(user.id))

    session.add(trip)
    session.commit()

    photo = Photo(**get_test_photo(author_id=user.id, trip_id=trip.id))

    session.add(photo)
    session.commit()

    fetched = session.get(Photo, photo.id)

    assert fetched is not None
    assert fetched.trip is not None
    assert fetched.trip == trip
    assert fetched.trip_id == trip.id


def test_create_photometadata(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    photo = Photo(**get_test_photo(user.id))

    session.add(photo)
    session.commit()

    photo_metadata = PhotoMetadata(photo_id=photo.id, camera_make="Fujifilm")

    session.add(photo_metadata)
    session.commit()

    assert session.get(PhotoMetadata, photo_metadata.photo_id) is not None
    assert session.get(PhotoMetadata, photo.id) is not None
    assert photo.photo_metadata is not None

    # Attempt second creation of photo_metadata (should not happen).
    # READ: shows a warning in the output as SQLAlchemy detects the identity conflict
    # at the Python level before you accidentally might make a database call.
    with pytest.raises(IntegrityError):  # Use this than try/except.
        photo_metadata2 = PhotoMetadata(photo_id=photo.id, camera_make="Sony")
        session.add(photo_metadata2)
        session.commit()

    session.rollback()

    assert session.get(PhotoMetadata, photo.id).camera_make == "Fujifilm"


def test_delete_photo_deletes_photometadata(session):
    """Photo and PhotoMetadata have a 1-1 relationship"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    photo = Photo(**get_test_photo(user.id))

    session.add(photo)
    session.commit()

    photo_metadata = PhotoMetadata(photo_id=photo.id, camera_make="Sony")

    session.add(photo_metadata)
    session.commit()

    photo_id = photo.id  # Save before deleting.

    session.delete(photo)
    session.commit()

    assert session.get(PhotoMetadata, photo_id) is None
