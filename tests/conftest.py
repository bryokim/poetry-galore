import os
import pytest

from flask_login import FlaskLoginClient

from app import create_app, db as app_db
from app.models.comment import Comment
from app.models.poem import Poem
from app.models.user import User


@pytest.fixture(scope="module")
def app(request):
    """Flask app"""

    # Set Testing configuration
    os.environ["APP_SETTINGS"] = "config.TestingConfig"

    app = create_app()
    ctx = app.app_context()
    ctx.push()

    yield app

    # Teardown
    ctx.pop()


@pytest.fixture(scope="function")
def db(app):
    """Database"""

    app_db.create_all()
    yield app_db

    # Teardown
    app_db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    """Client with no user logged in"""

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def test_user(db):
    """Test user"""

    user = User(
        username="One",
        email="one@one.com",
        password="12345678",
        unhashed_password="12345678",
    )
    db.session.add(user)
    db.session.commit()
    yield user

    # Teardown
    db.session.close()


@pytest.fixture(scope="function")
def test_poem(db, test_user):
    """Test poem"""

    poem = Poem(
        title="Hello Poetry Galore",
        body="Hello Poetry Galore",
        language="en",
        user_id=test_user.id,
    )
    db.session.add(poem)
    db.session.commit()
    yield poem

    # Teardown
    db.session.close()


@pytest.fixture(scope="function")
def test_comment(db, test_user, test_poem):
    """Test comment"""

    comment = Comment(
        text="Nice one", user_id=test_user.id, poem_id=test_poem.id
    )
    db.session.add(comment)
    db.session.commit()
    yield comment

    # Teardown
    db.session.close()


@pytest.fixture(scope="function")
def test_category(db):
    """Test category"""
    from app.models.category import Category

    category = Category(name="Classic")
    db.session.add(category)
    db.session.commit()
    yield category

    # Teardown
    db.session.close()


@pytest.fixture(scope="function")
def test_theme(db):
    """Test theme"""
    from app.models.theme import Theme

    theme = Theme(name="Happy")
    db.session.add(theme)
    db.session.commit()
    yield theme

    # Teardown
    db.session.close()


@pytest.fixture(scope="function")
def logged_in_user_client(app, db, test_user):
    """Client with user logged in"""

    # Set FlaskLoginClient that sets user's login cookie.
    app.test_client_class = FlaskLoginClient

    # client is automatically logged in with test_user
    with app.test_client(user=test_user) as client:
        yield client
