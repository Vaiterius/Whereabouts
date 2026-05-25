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
