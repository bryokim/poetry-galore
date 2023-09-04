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
from app.models.category import Category
from app.models.poem import Poem
from app.models.theme import Theme
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

    return render_template("poem.html", poem=poem)


def create_themes(themes_str):
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

    Returns:
        dict: The newly created poem.
    """

    form = PostPoemForm(request.form)
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

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: The updated poem.
    """
    form = PostPoemForm(request.form)
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
