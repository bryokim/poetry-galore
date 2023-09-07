"""Endpoints for dealing with comments.
"""
from datetime import datetime
from flask import (
    abort,
    render_template,
    request,
)
from flask_login import current_user, login_required

from app.views import core_view
from app.models.comment import Comment
from app.models.poem import Poem
from app.models.engine.db_storage import DBStorage


@core_view.route("/poems/<poem_id>/comments", methods=["POST"])
@login_required
def create_comment(poem_id):
    """Post a new comment.
    Users cannot comment twice on the same poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        Response: Render the poem.html template with the new
            comment having been added.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    if DBStorage().get_by_attribute(
        Comment, user_id=current_user.id, poem_id=poem_id
    ):
        return render_template("poem.html", poem=poem)

    data = {
        "poem_id": poem_id,
        "user_id": current_user.id,
        "text": request.form.get("comment"),
    }

    comment = Comment(**data)

    DBStorage().new(comment)
    DBStorage().save()

    return render_template("poem.html", poem=poem)


@core_view.route("/poems/<poem_id>/comments/<comment_id>/update")
@login_required
def update_comment(poem_id, comment_id):
    """Update a comment.
    User cannot update a comment that is not theirs.

    Args:
        poem_id (str): The poem id.
        comment_id (str): The comment id.

    Returns:
        Response: Render the poem.html template with the updated
            comment having been added.
    """
    poem = DBStorage().get(Poem, poem_id)
    comment = DBStorage().get(Comment, comment_id)
    text = request.args.get("text")

    comment.text = text
    comment.updated_at = datetime.utcnow()

    DBStorage().new(comment)
    DBStorage().save()

    return render_template("poem.html", poem=poem)


@core_view.route("/poems/<poem_id>/comments/<comment_id>/delete")
@login_required
def delete_comment(poem_id, comment_id):
    """Delete a comment.
    Users cannot delete comments that are not theirs.

    Args:
        poem_id (str): The poem id.
        comment_id (str): The comment id.

    Returns:
        Response: Render the poem.html template after having
            deleted the selected comment.
    """
    poem = DBStorage().get(Poem, poem_id)
    comment = DBStorage().get(Comment, comment_id)

    if not poem:
        abort(404)

    if not comment:
        render_template("poem.html", poem=poem)

    DBStorage().delete(comment)
    DBStorage().save()

    return render_template("poem.html", poem=poem)
