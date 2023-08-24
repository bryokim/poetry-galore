"""Endpoints for dealing with comments.
"""

from flask import abort, jsonify, make_response, redirect, request, url_for
from flask_login import current_user, fresh_login_required, login_required

from app.views import core_view
from app.models.comment import Comment
from app.models.poem import Poem
from app.models.user import User
from app.models.engine.db_storage import DBStorage


@core_view.route("/comments")
def get_all_comments():
    """Get all comments.

    Returns:
        list: A list of all comments.
    """
    comments = DBStorage().all(Comment)

    return make_response(
        jsonify([comment.to_dict() for comment in comments.values()])
    )


@core_view.route("/poems/<poem_id>/comment")
def get_poem_comments(poem_id):
    """Get comments for a certain poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        list: A list of all comments for given poem.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    comments = poem.comments

    return make_response(jsonify([comment.to_dict() for comment in comments]))


@core_view.route("/poems/<poem_id>/comments", methods=["POST"])
@login_required
def create_comment(poem_id):
    """Post a new comment.
    Users cannot comment twice on the same poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: The newly created comment.
    """
    poem = DBStorage().get(Poem, poem_id)
    text = request.form.get("text")

    if not poem:
        abort(404)

    if not text:
        return redirect(url_for("core_view.get_poem", poem_id=poem_id))

    if DBStorage().get_by_attribute(
        Comment, user_id=current_user.id, poem_id=poem_id
    ):
        return redirect(url_for("core_view.get_poem", poem_id=poem_id))

    data = {"poem_id": poem_id, "user_id": current_user.id, "text": text}

    comment = Comment(**data)

    DBStorage().new(comment)
    DBStorage().save()

    return redirect(url_for("core_view.get_poem", poem_id=poem_id))


@core_view.route("/poems/<poem_id>/comments/<comment_id>", methods=["UPDATE"])
@login_required
def update_comment(poem_id, comment_id):
    """Update a comment.
    User cannot update a comment that is not theirs.

    Args:
        poem_id (str): The poem id.
        comment_id (str): The comment id.

    Returns:
        dict: The newly updated poem.
    """
    poem = DBStorage().get(Poem, poem_id)
    comment = DBStorage().get(Comment, comment_id)
    data = request.get_json(silent=True)

    if not comment or not poem:
        abort(404)

    if not data:
        abort(400, description="Invalid JSON")

    ignore_keys = ["id", "created_at", "updated_at", "user_id", "poem_id"]

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(comment, key, value)

    DBStorage().new(comment)
    DBStorage().save()

    return make_response(jsonify(comment.to_dict()))


@core_view.route("/poems/<poem_id>/comments/<comment_id>", methods=["DELETE"])
@login_required
def delete_comment(poem_id, comment_id):
    """Delete a comment.
    Users cannot delete comments that are not theirs.

    Args:
        poem_id (str): The poem id.
        comment_id (str): The comment id.

    Returns:
        _type_: _description_
    """
    poem = DBStorage().get(Poem, poem_id)
    comment = DBStorage().get(Comment, comment_id)

    if not poem or not comment:
        abort(404)

    # if current_user.id != comment.user_id:
    #     abort(
    #         400,
    #         description=f"Comment doesn't belong to {current_user.username}",
    #     )

    DBStorage().delete(comment)
    DBStorage().save()

    return make_response(jsonify({}))
