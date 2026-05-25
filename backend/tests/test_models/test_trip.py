from app.models import Trip, User


from tests.conftest import get_test_user, get_test_trip


def test_create_trip(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    trip = Trip(**get_test_trip(author_id=user.id))

    session.add(trip)
    session.commit()

    fetched = session.get(Trip, trip.id)

    assert fetched is not None
