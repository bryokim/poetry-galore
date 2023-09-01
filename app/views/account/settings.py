from datetime import timedelta
from flask import (
    abort,
    current_app,
    flash,
    jsonify,
    make_response,
    request,
    redirect,
    render_template,
    url_for,
)
from flask_login import (
    login_required,
    fresh_login_required,
)

from app.models.user import User
from app.models.engine.db_storage import DBStorage
from app.forms.register import RegisterForm
from app.utils.decorators import logout_required
from app.views import accounts_view


@accounts_view.route("/settings")
@login_required
def user_settings():
    return render_template('accounts/settings.html')
