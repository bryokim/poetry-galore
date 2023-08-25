from datetime import timedelta
from flask import (
    flash,
    request,
    redirect,
    render_template,
    session,
    url_for,
)
from flask_login import login_user

from app import bcrypt
from app.models.user import User
from app.forms.login import LoginForm
from app.utils.decorators import logout_required
from app.views import accounts_view


@accounts_view.route("/login", methods=["GET", "POST"])
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

            if "next" in session:
                next_url = session["next"]
                del session["next"]
                return redirect(next_url)

            return redirect(url_for("accounts_view.home"))
        else:
            flash("Invalid email/password", "danger")
            return render_template("accounts/login.html", form=form)

    return render_template("accounts/login.html", form=form)
