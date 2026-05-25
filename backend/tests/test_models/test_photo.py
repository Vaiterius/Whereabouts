from app.models import Photo, User


from tests.conftest import get_test_user, get_test_photo


def test_create_photo(session):
    user = User(**get_test_user())

    session.add(user)
    session.commit()

    photo = Photo(**get_test_photo(author_id=user.id))

    session.add(photo)
    session.commit()

    fetched = session.get(Photo, photo.id)

    assert fetched is not None
