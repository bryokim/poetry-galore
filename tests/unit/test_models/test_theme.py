"""Tests for the Theme model"""

from app.models.theme import Theme


def test_new_theme():
    """
    GIVEN a Theme model
    WHEN a new theme is created
    THEN check that the name and attributes inherited
        from both the BaseModel class are defined correctly.
    """
    theme = Theme(name="Happy")

    assert theme.name == "Happy"

    # BaseModel properties
    assert theme.id is not None
    assert theme.created_at is not None
    assert theme.updated_at is not None


def test_theme_to_dict(test_theme):
    """
    GIVEN a Theme model
    WHEN the to_dict method is called
    THEN a dictionary of the model with a __class__ key with a value of
        Theme is returned. Check that both created_at and updated_at
        have been converted to isoformat.
    """
    theme = test_theme

    theme_dict = theme.to_dict()

    assert type(theme_dict) is dict

    assert theme_dict["__class__"] == "Theme"

    assert theme_dict["id"] is not None
    assert type(theme_dict["id"]) is str

    assert theme_dict["created_at"] is not None
    assert type(theme_dict["created_at"]) is str

    assert theme_dict["updated_at"] is not None
    assert type(theme_dict["updated_at"]) is str


def test_theme_save(db, test_theme):
    """
    GIVEN a Theme model
    WHEN save method is called
    THEN updated_at is updated and the theme is added to the database session
        and committed to the database.
    """
    before_save = test_theme.updated_at

    test_theme.save(db)

    after_save = test_theme.updated_at
    theme_in_database_after = (
        db.session.query(Theme).filter(Theme.id == test_theme.id).one()
    )

    assert before_save != after_save  # updated_at changed
    assert before_save < after_save

    assert before_save != theme_in_database_after.updated_at
    assert (
        after_save == theme_in_database_after.updated_at
    )  # theme was committed to database
