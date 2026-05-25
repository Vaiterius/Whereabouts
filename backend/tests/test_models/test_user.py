from app.models import User


def test_create_user(session):
    user = User(email="buashjd", first_name="asd", last_name="gdsfdad")
    session.add(user)
    session.commit()

    fetched = session.get(User, user.id)
    assert fetched is not None
