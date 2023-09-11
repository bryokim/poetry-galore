"""
Tests for the login page.
"""


def login(client, username, password):
    return client.post(
        "/login",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def test_login_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/login")
    assert b"Sign in" in response.data
    assert b"Remember me" in response.data


def test_login_post(client, db, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (POST) with correct credentials
    THEN check that the user is logged in successfully.
    """
    response = login(client, test_user.username, test_user.unhashed_password)
    assert b"You were logged in" in response.data
    assert b"Create" in response.data
    assert response.request.path == "/home"

    # Log out to ensure other login tests don't find a logged in user.
    logout(client)


def test_login_bad_username(client, db, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (POST) with invalid username
    THEN check that message is flashed on the login page and user
        is not logged in.
    """
    response = login(
        client, f"{test_user.username}x", test_user.unhashed_password
    )
    assert b"Invalid username/password" in response.data
    assert response.request.path == "/login"  # Doesn't redirect to home


def test_login_bad_password(client, db, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (POST) with invalid password
    THEN check that message is flashed on the login page and user
        is not logged in.
    """
    response = login(
        client, test_user.username, f"{test_user.unhashed_password}0"
    )
    assert b"Invalid username/password" in response.data
    assert response.request.path == "/login"  # Doesn't redirect to home
