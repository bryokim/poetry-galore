"""Test the DBStorage class"""

import pytest

from app.models.engine.db_storage import DBStorage


def test_db_storage_all_empty_db(db):
    """
    GIVEN a DBStorage class and an empty database
    WHEN the all method is called
    THEN an empty dictionary is returned.
    """
    storage = DBStorage(db)

    assert type(storage.all()) is dict
    assert len(storage.all()) == 0  # No objects in the database


def test_db_storage_all_populated_db(db, test_user, test_poem, test_comment):
    """
    GIVEN a DBStorage class and a populated database
    WHEN the all method is called
    THEN a dictionary of all objects in the database is returned.
    """
    storage = DBStorage(db)
    all_objects = storage.all()

    assert type(all_objects) is dict
    assert (
        len(all_objects) == 3
    )  # User, Poem and Comment objects as in args are returned


def test_db_storage_all_specific_class(db, test_user, test_poem, test_comment):
    """
    GIVEN a DBStorage class and a populated database
    WHEN the all method is called with a specific class
    THEN a dictionary of all objects of that class in the database is returned.
    """
    from app.models.user import User

    storage = DBStorage(db)
    all_objects = storage.all(User)  # Get only user objects.

    assert type(all_objects) is dict
    assert len(all_objects) == 1  # The user object created
    assert (
        type(list(all_objects.values())[0]) is User
    )  # Type of the object is user


def test_db_storage_new(db):
    """
    GIVEN a DBStorage class and a new object
    WHEN the new method is called with the newly created object
    THEN the object is added waiting to be committed to the database.
    """
    from app.models.user import User

    user = User(username="Two", email="user@example.com", password="password")

    storage = DBStorage(db)
    storage.new(user)  # Add the user to the database
    db.session.commit()  # Commit the changes

    assert len(db.session.query(User).all()) == 1

    with pytest.raises(TypeError):
        storage.new()  # Called without object being added


def test_db_storage_save(db):
    """
    GIVEN a DBStorage class and newly added object(s)
    WHEN the save method is called
    THEN the added object(s) are committed to the database.
    """
    from app.models.category import Category
    from app.models.theme import Theme
    from app.models.user import User

    storage = DBStorage(db)

    category = Category(name="New age")
    theme = Theme(name="Sad")
    user = User(username="Two", email="user@example.com", password="password")

    db.session.add(category)  # Add the category
    storage.save()  # Commit the category

    assert len(db.session.query(Category).all()) == 1

    db.session.add_all([theme, user])  # Add multiple objects
    storage.save()  # Commit the theme and user

    assert len(db.session.query(Theme).all()) == 1
    assert len(db.session.query(User).all()) == 1


def test_db_storage_delete(db, test_user):
    """
    GIVEN a DBStorage class
    WHEN the delete method is called with an object
    THEN if the object is found in the database, it is deleted.
    """
    from app.models.user import User

    storage = DBStorage(db)

    assert (
        db.session.query(User).one() is test_user
    )  # test_user is stored in the database

    storage.delete(test_user)  # Delete test_user from the database

    assert len(db.session.query(User).all()) == 0  # Test user has been deleted

    storage.delete()  # Called without an object. Nothing happens


def test_db_storage_get_good_id(db, test_user, test_poem):
    """
    GIVEN a DBStorage class, database model class and an id
    WHEN the get method is called with a class and a valid id
    THEN an object of that class with the given id is returned
    """
    from app.models.poem import Poem
    from app.models.user import User

    user_id = test_user.id
    poem_id = test_poem.id

    storage = DBStorage(db)

    user_gotten = storage.get(User, user_id)
    poem_gotten = storage.get(Poem, poem_id)

    assert user_gotten is test_user
    assert poem_gotten is test_poem


def test_db_storage_get_bad_id(db, test_user, test_poem):
    """
    GIVEN a DBStorage class, database model class and an id
    WHEN the get method is called with a class and an invalid id
    THEN None is returned
    """
    from app.models.poem import Poem
    from app.models.user import User

    user_id = test_user.id
    poem_id = test_poem.id

    storage = DBStorage(db)

    user_gotten = storage.get(User, poem_id)
    poem_gotten = storage.get(Poem, user_id)

    assert user_gotten is None
    assert poem_gotten is None


def test_db_storage_count_without_arg(db, test_user, test_poem, test_comment):
    """
    GIVEN a DBStorage class
    WHEN the count method is called without any arguments
    THEN the number of all objects in the database is returned
    """
    storage = DBStorage(db)

    assert storage.count() == 3  # test_user, test_poem and test_comment


def test_db_storage_count_with_arg(db, test_user, test_poem, test_comment):
    """
    GIVEN a DBStorage class
    WHEN the count method is called with a class argument
    THEN the number of objects of that class in the database is returned
    """
    from app.models.user import User
    from app.models.base_model import BaseModel

    storage = DBStorage(db)

    assert storage.count() == 3  # test_user, test_poem, test_comment
    assert storage.count(User) == 1  # test_user

    user = User(username="Two", email="user@example.com", password="password")
    db.session.add(user)
    db.session.commit()

    assert storage.count(User) == 2  # test_user and user


def test_db_storage_get_by_attribute(db, test_user, test_poem):
    """
    GIVEN a DBStorage class
    WHEN the get_by_attribute method is called with a class and kwargs
    THEN an object of that class whose properties match the kwargs is returned.
    """
    from app.models.poem import Poem
    from app.models.user import User

    storage = DBStorage(db)

    username = test_user.username
    email = test_user.email

    user_gotten = storage.get_by_attribute(
        User, **{"username": username, "email": email}
    )  # Get user using email and username

    assert user_gotten is test_user

    title = test_poem.title
    poem_gotten = storage.get_by_attribute(Poem, **{"title": title})

    assert poem_gotten is test_poem


def test_db_storage_get_by_attribute_bad_kwargs(db, test_user, test_poem):
    """
    GIVEN a DBStorage class
    WHEN the get_by_attribute method is called with a class and bad kwargs
    THEN None is returned. If the class doesn't have attribute in kwargs
        then AttributeError is raised.
    """
    from app.models.poem import Poem
    from app.models.user import User

    storage = DBStorage(db)

    username = test_user.username
    email = "email@invalid.com"  # invalid email address

    user_gotten = storage.get_by_attribute(
        User, **{"username": username, "email": email}
    )

    assert user_gotten is None

    with pytest.raises(AttributeError):
        poem_gotten = storage.get_by_attribute(
            Poem, **{"email": email}
        )  # email is not an attribute of a poem
