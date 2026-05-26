from app.models import User, Photo, Trip


from tests.conftest import get_test_user, get_test_photo, get_test_trip


def test_create_user(session):
    # All required fields.
    user = User(**get_test_user())
    # All fields.
    user2 = User(
        email="example2@gmail.com",
        first_name="Joe",
        last_name="Gatto",
        avatar_url="asjdasdasd",
        bio="asdasd",
    )
    session.add_all([user, user2])
    session.commit()

    fetched = session.get(User, user.id)
    assert fetched is not None
    assert fetched.id is not None
    assert fetched.created_at is not None
    assert fetched.avatar_url is None
    assert fetched.bio is None
    assert fetched.last_seen is None

    fetched2 = session.get(User, user2.id)
    assert fetched2 is not None
    assert fetched2.avatar_url is not None
    assert fetched2.bio is not None


def test_user_starts_with_no_photos(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    assert len(user.photos) == 0


def test_user_starts_with_no_trips(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    assert len(user.trips) == 0


def test_user_with_photos(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    photo1 = Photo(**get_test_photo(user.id))
    user.photos.append(photo1)

    session.commit()

    fetched_photo = session.get(Photo, photo1.id)

    assert fetched_photo is not None
    assert len(user.photos) == 1

    photo2 = Photo(**get_test_photo(user.id))
    photo3 = Photo(**get_test_photo(user.id))
    user.photos.extend([photo2, photo3])

    session.commit()

    assert len(user.photos) == 3


def test_user_with_trips(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip1 = Trip(**get_test_trip(user.id))
    trip2 = Trip(**get_test_trip(user.id))

    user.trips.extend([trip1, trip2])

    session.commit()

    assert len(user.trips) == 2


def test_user_photos_relationship_resolves(session):
    """Created photo's author id resolves back to the correct user"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    photo = Photo(**get_test_photo(user.id))
    user.photos.append(photo)

    session.commit()

    assert photo.author == user
    assert photo.author_id == user.id
    assert photo in user.photos


def test_user_trips_relationship_resolves(session):
    """Created trip's author id resolves back to the correct user"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(user.id))
    user.trips.append(trip)

    session.commit()

    assert trip.author == user
    assert trip.author_id == user.id
    assert trip in user.trips


def test_delete_user_deletes_photos(session):
    """Deleting user should cascade delete all their photos"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    photo = Photo(**get_test_photo(user.id))
    photo2 = Photo(**get_test_photo(user.id))
    photo3 = Photo(**get_test_photo(user.id))
    user.photos.extend([photo, photo2, photo3])

    session.commit()

    # Save before delete.
    photo_id = photo.id
    photo2_id = photo2.id
    photo3_id = photo3.id

    session.delete(user)
    session.commit()

    assert session.get(Photo, photo_id) is None
    assert session.get(Photo, photo2_id) is None
    assert session.get(Photo, photo3_id) is None


def test_delete_user_deletes_trips(session):
    """Deleting user should cascade delete all their trips"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(user.id))
    trip2 = Trip(**get_test_trip(user.id))
    # user.trips.extend([trip, trip2])
    session.add_all([trip, trip2])  # Same as above -- recommended.
    session.commit()

    # Save before delete.
    trip_id = trip.id
    trip2_id = trip2.id

    session.delete(user)
    session.commit()

    assert session.get(Trip, trip_id) is None
    assert session.get(Trip, trip2_id) is None


def test_delete_user_deletes_trips_with_photos(session):
    """Deleting a user should cascade delete all their trips and cascade deletes all its belonging photos as well"""
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(user.id))
    user.trips.append(trip)

    session.commit()

    photo = Photo(**get_test_photo(user.id, trip.id))
    photo2 = Photo(**get_test_photo(user.id, trip.id))
    photo3 = Photo(**get_test_photo(user.id, trip.id))
    photo4 = Photo(**get_test_photo(user.id))  # Not in a trip, should still be deleted.
    session.add_all([photo, photo2, photo3])

    session.commit()

    user_id = user.id
    trip_id = trip.id
    photo_id = photo.id
    photo2_id = photo2.id
    photo3_id = photo3.id
    photo4_id = photo4.id

    # Below comment: found out setting foreign key already updates photos list.
    # # I think we'll need to add the photos in both user.photos and trip.photos?
    # user.photos.extend([photo, photo2, photo3])
    # trip.photos.extend([photo, photo2, photo3])

    # assert user.photos == trip.photos
    # print(id(user.photos))
    # print(id(trip.photos))

    # print(user.photos)
    # print(trip.photos)

    assert user.photos == trip.photos  # Compares contents not memory addresses.

    session.delete(user)
    session.commit()

    assert session.get(User, user_id) is None
    assert session.get(Trip, trip_id) is None
    assert session.get(Photo, photo_id) is None
    assert session.get(Photo, photo2_id) is None
    assert session.get(Photo, photo3_id) is None
    assert session.get(Photo, photo4_id) is None
