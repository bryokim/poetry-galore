"""Module for the core_view poem routes.

These routes are used for rendering the web pages after doing some
operation depending on the request.

There are routes for creating, updating, retrieving and deleting
poems.
"""

from flask import (
    abort,
    redirect,
    request,
    render_template,
    url_for,
)
from flask_login import current_user, fresh_login_required, login_required

from app.views import core_view
from app.models.category import Category
from app.models.poem import Poem
from app.models.theme import Theme
from app.models.engine.db_storage import DBStorage
from app.forms.poem_form import PoemForm


@core_view.route("/poems/<poem_id>")
def get_poem(poem_id):
    """Get a specific poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        Response: Render the requested poem.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    return render_template("poem.html", poem=poem)


def create_themes(themes_str):
    """Create themes entered by the user while creating a new poem.
    If the theme already exists it is not created rather the existing
    one is returned.

    Args:
        themes_str (str): Comma separated string of the themes.

    Returns:
        list: A list of the theme objects to be added to the poem.
    """
    if not themes_str:
        return []

    theme_names = list(map(lambda x: x.strip().title(), themes_str.split(",")))

    theme_objs = []
    for name in theme_names:
        theme = DBStorage().get_by_attribute(Theme, name=name)

        if not theme:
            theme = Theme(name=name)
            DBStorage().new(theme)

        theme_objs.append(theme)

    DBStorage().save()

    return theme_objs


def create_category(category_name):
    """Create category entered by the user while creating a new poem.
    If the category already exists it is not created rather the existing
    one is returned.

    Args:
        category_name (str): Name of the category.

    Returns:
        list: A list of the category object to be added to the poem.
    """
    name = category_name.strip().title()

    category = DBStorage().get_by_attribute(Category, name=name)
    if not category:
        category = Category(name=name)
        DBStorage().new(category)
        DBStorage().save()

    return [category]


@core_view.route("/poems/create", methods=["GET", "POST"])
@login_required
def create_poem():
    """Post a poem.
    Themes and category selected during creation are added to the poem.
    If they are not present in the database, then they are first created
    and added to the poem.

    User has to be logged in for this operation to be successful.

    Returns:
        Response: Renders the post_poem.html template on a GET
            request and redirects to the get_poem endpoint on
            a POST request to render the created poem.
    """

    form = PoemForm(request.form)
    form.category.choices = [
        category.name for category in DBStorage().all(Category).values()
    ]

    if form.validate_on_submit():
        themes = create_themes(form.themes.data)
        category = create_category(form.category.data)

        new_poem = Poem(
            title=form.title.data,
            body=form.poem_body.data,
            user_id=current_user.id,
        )

        new_poem.themes = themes
        new_poem.category = category

        DBStorage().new(new_poem)
        DBStorage().save()

        return redirect(url_for("core_view.get_poem", poem_id=new_poem.id))

    return render_template(
        "post_poem.html",
        form=form,
        themes=list(DBStorage().all(Theme).values())[:12],
    )


@core_view.route("/poems/<poem_id>/update", methods=["GET", "POST"])
@login_required
def update_poem(poem_id: str):
    """Update a poem.
    User has to be logged in for this operation to be successful.

    Args:
        poem_id (str): The poem id.

    Returns:
        Response: Renders the update_poem.html template on a GET
            request and redirects to the get_poem endpoint on
            a POST request to render the updated poem.
    """
    form = PoemForm(request.form)
    form.category.choices = [
        category.name for category in DBStorage().all(Category).values()
    ]

    poem = DBStorage().get(Poem, poem_id)

    if request.method == "POST" and form.validate_on_submit():
        themes = create_themes(form.themes.data)
        category = create_category(form.category.data)

        poem.title = form.title.data
        poem.body = form.poem_body.data
        poem.themes = themes
        poem.category = category

        DBStorage().new(poem)
        DBStorage().save()

        return redirect(url_for("core_view.get_poem", poem_id=poem.id))
    else:
        category_name = ""
        if poem.category:
            category_name = poem.category[0].name

        theme_names = ""
        if poem.themes:
            theme_names = ", ".join([theme.name for theme in poem.themes])

        form.title.data = poem.title
        form.poem_body.data = poem.body
        form.themes.data = theme_names

    return render_template(
        "update_poem.html",
        form=form,
        category_name=category_name,
        themes=list(DBStorage().all(Theme).values())[:12],
    )


@core_view.route("/poems/<poem_id>/delete")
@login_required
def delete_poem(poem_id):
    """Delete a poem.
    User has to be logged in for this operation to be successful.

    Args:
        poem_id (str): The poem id.

    Returns:
        Response: Redirects to the home endpoint if user is
            deleted successfully.
    """
    poem = DBStorage().get(Poem, poem_id)

    DBStorage().delete(poem)
    DBStorage().save()

    return redirect(url_for("core_view.home"))
