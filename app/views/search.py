"""Module for searching logic applied to different elements."""

from flask import (
    abort,
    jsonify,
    make_response,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, fresh_login_required, login_required

from app.views import core_view
from app.models.category import Category
from app.models.poem import Poem
from app.models.theme import Theme
from app.models.engine.db_storage import DBStorage


@core_view.route("/search")
def search_poems():
    """Search for poems matching the query parameter search.
    The poem title is matched to the query parameter.

    Returns:
        response: Render home page with matching poems or
            if search parameter is empty, return all poems.
    """
    if request.args.get("search"):
        poems = DBStorage().all(Poem)
        search_text = request.args.get("search")
        valid_poems = {}

        for key, poem in poems.items():
            if search_text.lower() in poem.title.lower():
                valid_poems[key] = poem

        return render_template(
            "home.html",
            search=search_text,
            poems=valid_poems.values(),
            themes=DBStorage().all(Theme).values(),
        )
    else:
        return render_template(
            "home.html",
            poems=DBStorage().all(Poem).values(),
            themes=DBStorage().all(Theme).values(),
        )


@core_view.route("/search_by_theme", methods=["POST"])
def search_by_theme():
    """Search for poems by themes.

    Returns:
        List: List of all the invalid poem ids. These poem ids
        are used in hiding or showing poems not matching the search from
        the document.
    """
    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Invalid JSON")

    if data.get("themeIds") is None:
        abort(400, description="Missing themeIds")

    if not data.get("poemIds"):
        abort(400, description="Missing poemIds")

    themes = []
    for themeId in data.get("themeIds"):
        themes.append(DBStorage().get(Theme, themeId))

    invalid_poem_ids = []
    for poemId in data.get("poemIds"):
        poem = DBStorage().get(Poem, poemId)

        for theme in themes:
            if theme not in poem.themes:
                invalid_poem_ids.append(poemId)
                break

    return make_response(jsonify(invalid_poem_ids))
