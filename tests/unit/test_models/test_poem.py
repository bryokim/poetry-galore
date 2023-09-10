"""Tests for the Poem model"""

from app.models.poem import Poem


def test_new_poem(db, test_user):
    """
    GIVEN a Poem model
    WHEN a new poem is created
    THEN check the title, body, language, user_id and
        attributes inherited from both the BaseModel class
        are defined correctly.
    """
    user = test_user

    poem = Poem(
        title="Hello Poetry Galore",
        body="Hello Poetry Galore",
        language="en",
        user_id=user.id,
    )

    assert poem.title == "Hello Poetry Galore"
    assert poem.body == "Hello Poetry Galore"
    assert poem.language == "en"
    assert poem.user_id == user.id

    # BaseModel properties
    assert poem.id is not None
    assert poem.created_at is not None
    assert poem.updated_at is not None


def test_poem_to_dict(test_poem):
    """
    GIVEN a Poem model
    WHEN the to_dict method is called
    THEN a dictionary of the model with a __class__ key with a value of
        Poem is returned. Check that both created_at and updated_at
        have been converted to isoformat.
    """
    poem = test_poem

    poem_dict = poem.to_dict()

    assert type(poem_dict) is dict

    assert poem_dict["__class__"] == "Poem"

    assert poem_dict["id"] is not None
    assert type(poem_dict["id"]) is str

    assert poem_dict["created_at"] is not None
    assert type(poem_dict["created_at"]) is str

    assert poem_dict["updated_at"] is not None
    assert type(poem_dict["updated_at"]) is str


def test_poem_likes(test_poem, test_user):
    """
    GIVEN a Poem model and a User model
    WHEN the user is added to the poem's likes list
    THEN the length of the likes list increases by one and
        the poem is added to the user's user_likes list.
    """
    user = test_user
    poem = test_poem

    assert len(poem.likes) == 0  # Poem has no likes
    assert len(user.user_likes) == 0  # User has not liked any poem.

    poem.likes.append(user)  # User likes the poem
    assert len(poem.likes) == 1  # User added to likes
    assert len(user.user_likes) == 1  # Poem added to user's likes.

    assert poem.likes[0] is user
    assert user.user_likes[0] is poem


def test_poem_comments(test_poem, test_comment):
    """
    GIVEN a Poem model and a Comment model
    WHEN the comment is created
    THEN the comment is added to the comments list of the poem
        whose id is the poem_id in the comment and the poem is
        added to the comment's poem property.
    """
    poem = test_poem
    comment = test_comment

    assert len(poem.comments) == 1  # The created comment
    assert poem.comments[0] is comment
    assert (
        comment.poem is poem
    )  # The poem referenced in the poem_id attribute.


def test_poem_category(test_poem, test_category):
    """
    GIVEN a Poem model and a Category model
    WHEN the category is added to the poem's category list
    THEN the length of the category list increases by one and
        the poem is added to the category's poems list.
    """
    poem = test_poem
    category = test_category

    assert len(poem.category) == 0
    assert len(category.poems) == 0

    poem.category.append(category)

    assert len(poem.category) == 1
    assert len(category.poems) == 1
    assert category.poems[0] is poem


def test_poem_theme(test_poem, test_theme):
    """
    GIVEN a Poem model and a Theme model
    WHEN the theme is added to the poem's themes list
    THEN the length of the themes list increases by one and
        the poem is added to the theme's poems list.
    """
    poem = test_poem
    theme = test_theme

    assert len(poem.themes) == 0
    assert len(theme.poems) == 0

    poem.themes.append(theme)

    assert len(poem.themes) == 1
    assert len(theme.poems) == 1
    assert theme.poems[0] is poem


def test_poem_save(db, test_poem):
    """
    GIVEN a Poem model
    WHEN save method is called
    THEN updated_at is updated and the poem is added to the database session
        and committed to the database.
    """
    before_save = test_poem.updated_at

    test_poem.save(db)

    after_save = test_poem.updated_at
    poem_in_database_after = (
        db.session.query(Poem).filter(Poem.id == test_poem.id).one()
    )

    assert before_save != after_save  # updated_at changed
    assert before_save < after_save

    assert before_save != poem_in_database_after.updated_at
    assert (
        after_save == poem_in_database_after.updated_at
    )  # poem was committed to database
