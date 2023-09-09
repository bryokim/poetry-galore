from datetime import timedelta
from flask import (
    flash,
    request,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_user

from app.models.user import User
from app.models.engine.db_storage import DBStorage
from app.forms.register_form import RegisterForm
from app.utils.decorators import logout_required
from app.views import core_view


@core_view.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        DBStorage().new(user)
        DBStorage().save()

        # token = generate_token(user.email)
        # confirm_url = url_for(
        #     "accounts.confirm_email", token=token, _external=True
        # )
        # html = render_template(
        #     "confirm_email.html", confirm_url=confirm_url
        # )
        # subject = "Please confirm your email"
        # send_email(user.email, subject, html)

        login_user(user, duration=timedelta(minutes=1))
        # flash("A confirmation email has been sent via email", "success")

        # return redirect(url_for("accounts.inactive"))
        return redirect(url_for("core_view.login"))

    return render_template("register.html", form=form)
