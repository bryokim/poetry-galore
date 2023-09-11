from flask import abort, jsonify, make_response, url_for
from flask_login import current_user, login_required
from sqlalchemy import text

from app import db
from app.views import core_view
from app.models.poem import Poem
from app.models.user import User
from app.models.engine.db_storage import DBStorage


@core_view.route("/poems/<poem_id>/likes")
def get_poem_likes(poem_id):
    """Get the number of likes for a poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: A dictionary containing likes and poem id.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    num = len(
        db.session.execute(
            text("SELECT * FROM likes WHERE poem_id=:poem_id").bindparams(
                poem_id=poem_id
            )
        ).all()
    )

    return make_response(jsonify({"likes": num}), 200)


@core_view.route("/user/liked")
@login_required
def get_user_likes():
    """Get number of poems user has liked.

    Returns:
        dict: A dict of likes and the liked poems.
    """

    poem_user_id_tuple_list = db.session.execute(
        text("SELECT * FROM likes WHERE user_id=:user_id").bindparams(
            user_id=current_user.id
        )
    ).all()

    return make_response(
        jsonify(
            {
                "likes": len(poem_user_id_tuple_list),
                "poems": [
                    url_for(
                        "core_view.get_poem", poem_id=poem_id, _external=True
                    )
                    for poem_id, _ in poem_user_id_tuple_list
                ],
            }
        ),
        200,
    )


@core_view.route("/user/likes")
@login_required
def get_user_likes_received():
    """Get number of likes the user has received in all
    their poems.

    Returns:
        dict: A dict with a key of likes received.
    """

    likes_received = 0

    for poem in current_user.poems:
        likes_received += len(poem.likes)

    return make_response(
        jsonify(
            {
                "likes": likes_received,
            }
        ),
        200,
    )


@core_view.route("/poems/<poem_id>/like")
@login_required
def like_poem(poem_id):
    """Post a like for a poem by a user.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: The user that liked the poem.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    if current_user not in poem.likes:
        poem.likes.append(current_user)
        DBStorage().new(poem)
        DBStorage().save()

    num = len(
        db.session.execute(
            text("SELECT * FROM likes WHERE poem_id=:poem_id").bindparams(
                poem_id=poem_id
            )
        ).all()
    )

    return make_response(jsonify({"likes": num}), 200)


@core_view.route("/poems/<poem_id>/unlike")
@login_required
def unlike_poem(poem_id):
    """Delete a like for a poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: An empty dictionary.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem or current_user not in poem.likes:
        abort(404)
    else:
        poem.likes.remove(current_user)
        DBStorage().new(poem)
        DBStorage().save()

    num = len(
        db.session.execute(
            text("SELECT * FROM likes WHERE poem_id=:poem_id").bindparams(
                poem_id=poem_id
            )
        ).all()
    )

    return make_response(jsonify({"likes": num}), 200)
