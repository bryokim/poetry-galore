from flask import (
    abort,
    jsonify,
    make_response,
    redirect,
    request,
    render_template,
    url_for,
)
from flask_login import current_user, fresh_login_required, login_required

from app.views import core_view
from app.models.poem import Poem
from app.models.user import User
from app.models.engine.db_storage import DBStorage
from app.forms.post_poem import PostPoemForm


@core_view.route("/poems")
def get_poems():
    """Get all poems.

    Returns:
        list: List of all the poems.
    """
    poems = DBStorage().all(Poem)
    poems_dictionaries = [poem.to_dict() for poem in poems.values()]

    for poem in poems_dictionaries:
        poem["url"] = url_for(
            "core_view.get_poem", poem_id=poem["id"], _external=True
        )
        del poem["id"]

        poem["user"] = (
            DBStorage().get(User, poem["user_id"]).to_dict(password=False)
        )

        poem["user"]["url"] = url_for(
            "core_view.get_user", user_id=poem["user_id"], _external=True
        )
        del poem["user_id"]
        del poem["user"]["id"]

    return make_response(jsonify(poems_dictionaries), 200)


@core_view.route("/poems/<poem_id>")
def get_poem(poem_id):
    """Get a specific poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: The requested poem.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    return render_template("core/poem.html", poem=poem)


@core_view.route("/poems/create", methods=["GET", "POST"])
@login_required
def create_poem():
    """Post a poem.

    Returns:
        dict: The newly created poem.
    """

    form = PostPoemForm(request.form)

    if form.validate_on_submit():
        new_poem = Poem(
            title=form.title.data,
            body=form.poem_body.data,
            user_id=current_user.id,
        )

        DBStorage().new(new_poem)
        DBStorage().save()

        return redirect(url_for("core_view.get_poem", poem_id=new_poem.id))

    return render_template("accounts/post_poem.html", form=form)


@core_view.route("/poems/<poem_id>", methods=["UPDATE"])
@login_required
def update_poem(poem_id: str):
    """Update a poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: The updated poem.
    """
    data = request.get_json(silent=True)
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    if not data:
        abort(400, description="Invalid JSON")

    ignore_keys = ["id", "created_at", "updated_at", "user_id"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(poem, key, value)

    DBStorage().new(poem)
    DBStorage().save()

    return make_response(jsonify(poem.to_dict()), 200)


@core_view.route("/poems/<poem_id>/delete")
@login_required
def delete_poem(poem_id):
    """Delete a poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: An empty dictionary.
    """
    poem = DBStorage().get(Poem, poem_id)

    # if not poem:
    #     abort(404)

    DBStorage().delete(poem)
    DBStorage().save()

    return redirect(url_for("accounts_view.home"))
