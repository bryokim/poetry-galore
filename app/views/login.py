from datetime import timedelta
from decouple import config
from flask import (
    flash,
    request,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_user


from app import bcrypt
from app.models.user import User
from app.forms.login_form import LoginForm
from app.utils.decorators import logout_required
from app.views import core_view


@core_view.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            if form.remember_me.data:
                login_user(user, remember=True, duration=timedelta(minutes=30))
            else:
                login_user(user)

            if "next" in request.args:
                next_url = request.args["next"]
                return redirect(next_url)

            return redirect(url_for("core_view.home"))
        else:
            flash("Invalid username/password", "danger")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)
