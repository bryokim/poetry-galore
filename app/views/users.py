from flask import (
    abort,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, fresh_login_required, login_required
from uuid import uuid4

from app import bcrypt
from app.views import core_view
from app.models.user import User
from app.models.engine.db_storage import DBStorage
from app.forms.update_details import UpdateUserForm


@core_view.route("/users")
def get_users():
    """Get a list of users.

    Returns:
        list: List of all users.
    """
    users = DBStorage().all(User)

    users_dictionaries = [
        user.to_dict(password=False) for user in users.values()
    ]

    for user_dict, user_obj in zip(users_dictionaries, users.values()):
        user_dict["url"] = url_for(
            "core_view.get_user", user_id=user_dict["id"], _external=True
        )
        del user_dict["id"]

        user_dict["poems"] = [
            url_for("core_view.get_poem", poem_id=poem.id, _external=True)
            for poem in user_obj.poems
        ]

    return make_response(jsonify(users_dictionaries))


@core_view.route("/users/<username>")
def get_user_profile(username):
    # user = DBStorage().get_by_attribute(User, username=username)

    # print(username)
    # if not user:
    #     return redirect(url_for("accounts_view.home"))

    response = make_response(
        render_template(
            "profile.html",
            user=current_user,
        )
    )

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Cache-Control"] = "public, max-age=0"

    return response


@core_view.route("/users/validate/username/<username>")
def validate_username(username):
    user = DBStorage().get_by_attribute(User, username=username)

    if not user:
        return make_response(jsonify({"error": "Invalid username"}))
    else:
        return make_response(jsonify({"success": "Username found"}))


@core_view.route("/users/validate/email/<email>")
def validate_email(email):
    user = DBStorage().get_by_attribute(User, email=email)

    if not user:
        return make_response(jsonify({"error": "Invalid email"}))
    else:
        return make_response(jsonify({"success": "Email found"}))


@core_view.route("/users/<user_id>")
@login_required
def get_user(user_id: str):
    """Get a user by user_id.

    Args:
        user_id (str): The user id.

    Returns:
        dict: The requested user.
    """
    # user = DBStorage().get(User, user_id)

    # if not user:
    #     abort(404)

    return redirect(
        url_for("core_view.get_user_profile", username=current_user.username)
    )


@core_view.route("/users", methods=["POST"])
def create_user():
    """Create a new user.

    Returns:
        dict: The newly created user.
    """
    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Invalid JSON")

    if not data.get("username"):
        abort(400, description="Must provide username")

    if not data.get("email"):
        abort(400, description="Must provide email")

    if not data.get("password"):
        abort(400, description="Must provide password")

    new_user = User(**data)

    DBStorage().new(new_user)
    DBStorage().save()

    return make_response(jsonify(new_user.to_dict()), 201)


@core_view.route("/users/update", methods=["GET", "POST"])
@fresh_login_required
def update_user():
    """Update a user.

    Args:
        user_id (str): The user id.

    Returns:
        dict: Newly updated user.
    """

    if request.method == "POST":
        current_user.username = (
            request.form.get("username") or current_user.username
        )
        current_user.email = request.form.get("email") or current_user.email

        if request.form.get("password") and request.form.get(
            "current-password"
        ):
            if bcrypt.check_password_hash(
                current_user.password, request.form.get("current-password")
            ):
                current_user.password = bcrypt.generate_password_hash(
                    request.form.get("password")
                )
                current_user.alternative_id = str(uuid4())
                flash("Password changed", "info")
            else:
                flash("Invalid password", "danger")

        DBStorage().new(current_user)
        DBStorage().save()

    return render_template("settings.html")


@core_view.route("/users/<user_id>", methods=["DELETE"])
@fresh_login_required
def delete_user(user_id: str):
    """Delete a user.

    Args:
        user_id (str): The user id.

    Returns:
        dict: An empty dictionary.
    """
    user = DBStorage().get(User, user_id)

    if not user:
        abort(404)

    DBStorage().delete(user)
    DBStorage().save()

    return make_response(jsonify({}), 200)
