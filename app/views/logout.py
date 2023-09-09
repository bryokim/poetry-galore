from flask import flash, redirect, url_for
from flask_login import login_required, logout_user

from app.views import core_view


@core_view.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("core_view.login"))
