from app.models import Trip, User, Photo


from tests.conftest import get_test_user, get_test_trip, get_test_photo


def test_create_trip(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(author_id=user.id))

    session.add(trip)
    session.commit()

    fetched = session.get(Trip, trip.id)

    assert fetched is not None
    assert trip.cover_photo is None
    assert trip.author == user


def test_create_trip_with_photos(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(author_id=user.id))

    session.add(trip)
    session.commit()

    photo = Photo(**get_test_photo(user.id, trip.id))
    photo2 = Photo(**get_test_photo(user.id, trip.id))
    photo3 = Photo(**get_test_photo(user.id, trip.id))

    session.add_all([photo, photo2, photo3])
    session.commit()

    assert len(trip.photos) == 3
    assert photo.trip == trip


def test_add_cover_photo(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(author_id=user.id))

    session.add(trip)
    session.commit()

    photo = Photo(**get_test_photo(user.id, trip.id))
    photo2 = Photo(**get_test_photo(user.id, trip.id))

    session.add_all([photo, photo2])
    session.commit()

    assert trip.cover_photo is None

    trip.cover_photo = photo

    session.commit()  # Updates foreign key cover_photo_id.

    assert trip.cover_photo is not None
    assert trip.cover_photo is photo
    assert trip.cover_photo is not photo2
    assert trip.cover_photo_id == photo.id

    session.expire_all()
    fetched = session.get(Trip, trip.id)

    assert fetched.cover_photo is photo
    assert fetched.cover_photo_id == photo.id

    # Replace cover photo.
    trip.cover_photo = photo2

    session.commit()

    session.expire_all()
    fetched = session.get(Trip, trip.id)

    assert fetched.cover_photo is not None
    assert fetched.cover_photo == photo2
    assert fetched.cover_photo is not photo
    assert fetched.cover_photo_id == photo2.id


def test_delete_trip_with_photos(session):
    """Deleting a trip should cascade delete all its photos"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(author_id=user.id))

    session.add(trip)
    session.commit()

    photo = Photo(**get_test_photo(user.id, trip.id))
    photo2 = Photo(**get_test_photo(user.id, trip.id))
    photo3 = Photo(**get_test_photo(user.id, trip.id))
    photo4 = Photo(**get_test_photo(user.id))

    # Save before deleting.
    photo_id = photo.id
    photo2_id = photo2.id
    photo3_id = photo3.id
    photo4_id = photo4.id

    session.add_all([photo, photo2, photo3, photo4])
    session.commit()

    assert photo in trip.photos
    assert photo.trip == trip
    assert len(trip.photos) == 3

    session.delete(trip)
    session.commit()

    from sqlalchemy import select

    remaining = session.execute(select(Photo)).scalars().all()
    print(remaining)  # what's actually in the DB?

    # One photo should still be left undeleted as it was unbound to any trip.
    assert session.get(Photo, photo_id) is None
    assert session.get(Photo, photo2_id) is None
    assert session.get(Photo, photo3_id) is None
    assert session.get(Photo, photo4_id) is not None
