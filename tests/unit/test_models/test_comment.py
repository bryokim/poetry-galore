"""Tests for the comment model"""

from app.models.comment import Comment


def test_new_comment(test_user, test_poem):
    """
    GIVEN a Comment model
    WHEN a new model is created
    THEN check that the text, user_id, poem_id and attributes
        inherited from BaseModel have been assigned correctly.
    """
    comment = Comment(
        text="Nice one", user_id=test_user.id, poem_id=test_poem.id
    )

    assert comment.text == "Nice one"
    assert comment.user_id == test_user.id
    assert comment.poem_id == test_poem.id

    # Inherited from BaseModel
    assert comment.id is not None
    assert comment.created_at is not None
    assert comment.updated_at is not None


def test_comment_to_dict(test_comment):
    """
    GIVEN a Comment model
    WHEN the to_dict method is called
    THEN a dictionary of the model with a __class__ key with a value of
        Comment is returned. Check that both created_at and updated_at
        have been converted to isoformat.
    """
    comment = test_comment

    comment_dict = comment.to_dict()

    assert type(comment_dict) is dict

    assert comment_dict["__class__"] == "Comment"

    assert comment_dict["id"] is not None
    assert type(comment_dict["id"]) is str

    assert comment_dict["created_at"] is not None
    assert type(comment_dict["created_at"]) is str

    assert comment_dict["updated_at"] is not None
    assert type(comment_dict["updated_at"]) is str


def test_comment_save(db, test_comment):
    """
    GIVEN a Category model
    WHEN save method is called
    THEN updated_at is updated and the comment is added to the database session
        and committed to the database.
    """
    before_save = test_comment.updated_at

    test_comment.save(db)

    after_save = test_comment.updated_at
    comment_in_database_after = (
        db.session.query(Comment).filter(Comment.id == test_comment.id).one()
    )

    assert before_save != after_save  # updated_at changed
    assert before_save < after_save

    assert before_save != comment_in_database_after.updated_at
    assert (
        after_save == comment_in_database_after.updated_at
    )  # comment was committed to database
