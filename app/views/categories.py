"""
Endpoints for the category model.
"""

from flask import render_template

from app.views import core_view
from app.models.category import Category
from app.models.theme import Theme
from app.models.engine.db_storage import DBStorage


@core_view.route("/categories/<category_id>/poems")
def get_poems_in_category(category_id):
    """Get poems linked to a certain category.

    Args:
        category_id (str): The category id.

    Returns:
        Response: Renders the home.htm template with poems
            in the given category.
    """
    category = DBStorage().get(Category, category_id)

    return render_template(
        "home.html",
        category_search=category.name,
        poems=category.poems,
        themes=DBStorage().all(Theme).values(),
        categories=DBStorage().all(Category).values(),
    )
