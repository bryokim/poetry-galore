"""Tests for the Category model"""

from app.models.category import Category


def test_new_category():
    """
    GIVEN a Category model
    WHEN a new category is created
    THEN check that the name and attributes inherited
        from BaseModel have been assigned correctly.
    """
    category = Category(name="Classic")

    assert category.name == "Classic"

    # Inherited from BaseModel
    assert category.id is not None
    assert category.created_at is not None
    assert category.updated_at is not None


def test_category_to_dict(test_category):
    """
    GIVEN a Category model
    WHEN the to_dict method is called
    THEN a dictionary of the model with a __class__ key with a value of
        Category is returned. Check that both created_at and updated_at
        have been converted to isoformat.
    """
    category = test_category

    category_dict = category.to_dict()

    assert type(category_dict) is dict

    assert category_dict["__class__"] == "Category"

    assert category_dict["id"] is not None
    assert type(category_dict["id"]) is str

    assert category_dict["created_at"] is not None
    assert type(category_dict["created_at"]) is str

    assert category_dict["updated_at"] is not None
    assert type(category_dict["updated_at"]) is str


def test_category_save(db, test_category):
    """
    GIVEN a Category model
    WHEN save method is called
    THEN updated_at is updated and the category is added to the database
        session and committed to the database.
    """
    before_save = test_category.updated_at

    test_category.save(db)

    after_save = test_category.updated_at
    category_in_database_after = (
        db.session.query(Category)
        .filter(Category.id == test_category.id)
        .one()
    )

    assert before_save != after_save  # updated_at changed
    assert before_save < after_save

    assert before_save != category_in_database_after.updated_at
    assert (
        after_save == category_in_database_after.updated_at
    )  # category was committed to database
