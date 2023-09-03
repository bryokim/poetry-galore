from flask import (
    abort,
    jsonify,
    make_response,
    render_template,
    request,
    url_for,
    current_app,
    session,
)
from flask_login import current_user, fresh_login_required, login_required

from app.views import core_view
from app.models.category import Category
from app.models.poem import Poem
from app.models.theme import Theme
from app.models.engine.db_storage import DBStorage


@core_view.route("/categories")
def get_categories():
    """Get all categories.

    Returns:
        list: A list of all categories.
    """
    categories = DBStorage().all(Category)

    return make_response(
        jsonify([category.to_dict() for category in categories.values()])
    )


@core_view.route("/categories/<category_id>")
def get_category(category_id):
    """Get a specific category.

    Args:
        category_id (str): The category id.

    Returns:
        dict: The category object dictionary.
    """
    category = DBStorage().get(Category, category_id)

    if not category:
        abort(404)

    return make_response(jsonify(category.to_dict()))


@core_view.route("/categories/<category_id>/poems")
def get_poems_in_category(category_id):
    """Get poems linked to a certain category.

    Args:
        category_id (str): The category id.

    Returns:
        list: A list of poems in that category.
    """
    category = DBStorage().get(Category, category_id)

    # if not category:
    #     abort(404)

    return render_template(
        "accounts/home.html",
        poems=category.poems,
        themes=DBStorage().all(Theme).values(),
        categories=DBStorage().all(Category).values(),
    )


@core_view.route("/categories", methods=["POST"])
def create_category():
    """Create a new category.

    Returns:
        dict: A dictionary of the newly created category.
    """
    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Invalid JSON")

    if not data.get("name"):
        abort(400, description="Missing name")

    data["name"] = data["name"].strip().title()
    if DBStorage().get_by_attribute(Category, name=data.get("name")):
        abort(400, description="Category already registered")

    category = Category(**data)

    DBStorage().new(category)
    DBStorage().save()

    return make_response(jsonify(category.to_dict()), 201)


@core_view.route("/poems/<poem_id>/categories/<category_id>", methods=["POST"])
def add_poem_category(poem_id, category_id):
    """Add a category to a certain poem.

    Args:
        poem_id (str): The poem id.
        category_id (str): The category id.

    Returns:
        dict: Dictionary of the added category.
    """
    category = DBStorage().get(Category, category_id)
    poem = DBStorage().get(Poem, poem_id)

    if not poem or not category:
        abort(404)

    if category not in poem.category:
        poem.category.append(category)
        DBStorage().new(poem)
        DBStorage().save()
        return make_response(jsonify(category.to_dict()), 201)
    elif category in poem.category:
        return make_response(jsonify(category.to_dict()), 200)


@core_view.route(
    "/poems/<poem_id>/categories/<category_id>", methods=["DELETE"]
)
def remove_poem_category(poem_id, category_id):
    """Delete a category to a certain poem.

    Args:
        poem_id (str): The poem id.
        category_id (str): The category id.

    Returns:
        dict: An empty dictionary.
    """
    category = DBStorage().get(Category, category_id)
    poem = DBStorage().get(Poem, poem_id)

    if not poem or not category:
        abort(404)

    if category in poem.category:
        poem.category.remove(category)
        DBStorage().new(poem)
        DBStorage().save()

    return make_response(jsonify({}), 200)
