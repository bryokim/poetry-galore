from flask import render_template

from app.views import accounts_view
from app.models.poem import Poem
from app.models.theme import Theme
from app.models.engine.db_storage import DBStorage


@accounts_view.route("/home")
def home():
    return render_template(
        "accounts/home.html",
        poems=DBStorage().all(Poem).values(),
        themes=DBStorage().all(Theme).values(),
    )
