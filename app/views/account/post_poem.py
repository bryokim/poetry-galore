# from datetime import datetime, timedelta
# from flask import (
#     flash,
#     request,
#     redirect,
#     render_template,
#     url_for,
# )
# from flask_login import login_user, login_required

# from app import bcrypt
# from app.models.user import User
# from app.forms.login import LoginForm
# from app.utils.decorators import logout_required
# from app.views import accounts_view


# @accounts_view.route("/post_poem")
# @login_required
# def post_poem():
#     return render_template("accounts/post_poem.html", form=form)
