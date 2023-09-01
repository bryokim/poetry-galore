from flask import abort, jsonify, make_response, request, url_for
from flask_login import current_user, login_required

from app.views import core_view
from app.models.theme import Theme
from app.models.poem import Poem
from app.models.engine.db_storage import DBStorage


@core_view.route("/themes")
def get_themes():
    """Get all themes.

    Returns:
        list: A list of all themes.
    """
    themes = DBStorage().all(Theme)

    return make_response(
        jsonify([theme.to_dict() for theme in themes.values()])
    )


@core_view.route("/themes/<theme_id>")
def get_theme(theme_id):
    """Get a theme by id.

    Args:
        theme_id (str): The theme id.

    Returns:
        dict: A dict of the requested theme.
    """
    theme = DBStorage().get(Theme, theme_id)

    if not theme:
        abort(404)

    return make_response(jsonify(theme.to_dict()))


@core_view.route("/themes/<theme_id>/poems")
def get_poems_with_theme(theme_id):
    """Get poems linked to a certain theme.

    Args:
        theme_id (str): The theme id.

    Returns:
        list: A list of poems with that theme.
    """
    theme = DBStorage().get(Theme, theme_id)

    if not theme:
        abort(404)

    return make_response(jsonify([poem.to_dict() for poem in theme.poems]))


@core_view.route("/themes", methods=["POST"])
# @login_required
def create_theme():
    """Create a new theme.

    Returns:
        dict: The new theme.
    """
    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Invalid JSON")

    if not data.get("name"):
        abort(400, description="Missing name")

    data["name"] = data["name"].strip().title()
    if DBStorage().get_by_attribute(Theme, name=data["name"]):
        abort(400, description="Theme already exists")

    theme = Theme(**data)

    DBStorage().new(theme)
    DBStorage().save()

    return make_response(jsonify(theme.to_dict()), 201)


@core_view.route("/poems/<poem_id>/themes/<theme_id>", methods=["POST"])
# @login_required
def add_poem_theme(poem_id, theme_id):
    """Add a theme to a given poem.

    Args:
        poem_id (str): The poem id.
        theme_id (str): The theme id.

    Returns:
        dict: A dictionary of the added theme.
    """
    poem = DBStorage().get(Poem, poem_id)
    theme = DBStorage().get(Theme, theme_id)

    if not poem or not theme:
        abort(404)

    if theme not in poem.themes:
        poem.themes.append(theme)
        DBStorage().new(poem)
        DBStorage().save()
        return make_response(jsonify(theme.to_dict()), 201)
    elif theme in poem.themes:
        return make_response(jsonify(theme.to_dict()), 200)


@core_view.route("/poems/<poem_id>/themes/<theme_id>", methods=["DELETE"])
@login_required
def remove_poem_theme(poem_id, theme_id):
    """Removes a theme from a poem.

    Args:
        poem_id (str): The poem id.
        theme_id (str): The theme id.

    Returns:
        dict: An empty dictionary.
    """
    poem = DBStorage().get(Poem, poem_id)
    theme = DBStorage().get(Theme, theme_id)

    if not poem or not theme:
        abort(404)

    if theme in poem.themes:
        poem.themes.remove(theme)
        DBStorage().new(poem)
        DBStorage().save()

    return make_response(jsonify({}), 200)
