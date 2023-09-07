from flask import render_template

from app.views import core_view
from app.models.category import Category
from app.models.poem import Poem
from app.models.theme import Theme
from app.models.engine.db_storage import DBStorage


@core_view.route("/home")
def home():
    return render_template(
        "home.html",
        poems=DBStorage().all(Poem).values(),
        themes=DBStorage().all(Theme).values(),
        categories=DBStorage().all(Category).values(),
    )
