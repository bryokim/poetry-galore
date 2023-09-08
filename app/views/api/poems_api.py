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

from app.views import api_view
from app.models.category import Category
from app.models.poem import Poem
from app.models.theme import Theme
from app.models.user import User
from app.models.engine.db_storage import DBStorage
from app.forms.poem_form import PoemForm


@api_view.route("/poems")
def get_poems():
    """Get all poems.

    Returns:
        list: List of all the poems.
    """
    poems = DBStorage().all(Poem)
    poems_dictionaries = [poem.to_dict() for poem in poems.values()]

    for poem in poems_dictionaries:
        poem["url"] = url_for(
            "api_view.get_poem", poem_id=poem["id"], _external=True
        )
        del poem["id"]

        poem["user"] = (
            DBStorage().get(User, poem["user_id"]).to_dict(password=False)
        )

        poem["user"]["url"] = url_for(
            "api_view.get_user", user_id=poem["user_id"], _external=True
        )
        del poem["user_id"]
        del poem["user"]["id"]

    return make_response(jsonify(poems_dictionaries), 200)
