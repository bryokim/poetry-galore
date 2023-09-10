"""Tests for the user model."""

import pytest

from app.models.user import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new user is created
    THEN check the username, email, password, alternative_id and
        attributes inherited from both the BaseModel class and UserMixin
        are defined correctly.
    """
    user = User(username="One", email="one@one.com", password="12345678")

    assert user.username == "One"
    assert user.email == "one@one.com"
    assert user.password != "12345678"  # Must be hashed
    assert user.alternative_id is not None
    assert type(user.alternative_id) is str

    # BaseModel properties
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None

    # UserMixin properties and methods
    assert user.is_active is True
    assert user.is_authenticated is True
    assert user.is_anonymous is False
    assert (
        user.get_id() == user.alternative_id
    )  # Overridden by the method in User class


def test_new_user_without_kwargs():
    """
    GIVEN a User model
    WHEN a new user is created without the kwargs
    THEN check that the initialization raises a ValueError
    """
    with pytest.raises(ValueError):
        user = User("One", "one@one.com", "12345678")


def test_user_to_dict(test_user):
    """
    GIVEN a User model
    WHEN the to_dict method is called
    THEN a dictionary of the model with a __class__ key with a value of
        User is returned. Check that both created_at and updated_at
        have been converted to isoformat.
    """
    user = test_user
    user_dict = user.to_dict()

    assert type(user_dict) is dict

    assert user_dict["__class__"] == "User"

    assert user_dict["id"] is not None
    assert type(user_dict["id"]) is str

    assert user_dict["created_at"] is not None
    assert type(user_dict["created_at"]) is str

    assert user_dict["updated_at"] is not None
    assert type(user_dict["updated_at"]) is str


def test_user_get_id(test_user):
    """
    GIVEN a User model
    WHEN the get_id method is called
    THEN the alternative_id is returned
    """
    assert test_user.get_id() == test_user.alternative_id


def test_user_likes(test_poem, test_user):
    """
    GIVEN a Poem model and a User model
    WHEN the poem is added to the user's user_likes list
    THEN the length of the user_likes list increases by one and
        the user is added to the poem's likes list.
    """
    user = test_user
    poem = test_poem

    assert len(poem.likes) == 0  # Poem has no likes
    assert len(user.user_likes) == 0  # User has not liked any poem.

    user.user_likes.append(poem)  # User likes the poem
    assert len(user.user_likes) == 1  # Poem added to user's likes.
    assert len(poem.likes) == 1  # User added to likes

    assert poem.likes[0] is user
    assert user.user_likes[0] is poem


def test_user_poems_relationship(test_user, test_poem):
    """
    GIVEN a User and Poem model
    WHEN a User creates a new Poem
    THEN the poem is added to the user's poems list
        and the user is added to the user property of the Poem
    """
    user = test_user
    poem = test_poem  # Created by test_user

    assert user.poems[0] is poem
    assert poem.user is user


def test_user_comments_relationship(test_user, test_comment):
    """
    GIVEN a User and Comment model
    WHEN a User creates a new Comment
    THEN the comment is added to the user's comments list
        and the user is added to the user property of the Comment
    """
    user = test_user
    comment = test_comment  # Created by test_user

    assert user.comments[0] is comment
    assert comment.user is user


def test_user_save(db, test_user):
    """
    GIVEN a User model
    WHEN save method is called
    THEN updated_at is updated and the user is added to the database session
        and committed to the database.
    """
    before_save = test_user.updated_at

    test_user.save(db)

    after_save = test_user.updated_at
    user_in_database_after = (
        db.session.query(User).filter(User.id == test_user.id).one()
    )

    assert before_save != after_save  # updated_at changed
    assert before_save < after_save

    assert before_save != user_in_database_after.updated_at
    assert (
        after_save == user_in_database_after.updated_at
    )  # user was committed to database
