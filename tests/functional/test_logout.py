"""
Tests for the logout page.
"""


def logout(client):
    """Logout a user"""
    return client.get("/logout", follow_redirects=True)


def test_logout(logged_in_user_client, db, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET) when user is logged in
    THEN check that the user is logged out successfully.
    """
    response = logout(logged_in_user_client)
    assert b"You were logged out" in response.data
    assert b"Login" in response.data
    assert response.request.path == "/login"  # Redirected to login


def test_logout_no_user_logged_in(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET) when user is not logged in
    THEN check that the user is alerted that they are required to
        be logged in and redirected to the login page.
    """
    response = logout(client)
    assert b"Login required" in response.data
    assert response.request.path == "/login"  # Redirected to login
