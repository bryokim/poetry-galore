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
import json
from oauthlib.oauth2 import WebApplicationClient
import requests

from app import bcrypt
from app.models.user import User
from app.forms.login_form import LoginForm
from app.utils.decorators import logout_required
from app.views import accounts_view
from app.views import core_view
from app.models.engine.db_storage import DBStorage


GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


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

            if "next" in request.args:
                next_url = request.args["next"]
                return redirect(next_url)

            return redirect(url_for("core_view.home"))
        else:
            flash("Invalid username/password", "danger")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@accounts_view.route("/login_by_google")
def login_by_google():
    goggle_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = goggle_provider_cfg["authorization_endpoint"]

    print(request.base_url)

    client = WebApplicationClient(config("GOOGLE_CLIENT_ID"))
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@accounts_view.route("/login_by_google/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    client = WebApplicationClient(config("GOOGLE_CLIENT_ID"))
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = DBStorage().get(User, unique_id)
    if not user:
        user = User(
            id=unique_id,
            username=users_name,
            email=users_email,
            password="00000000",
        )
        DBStorage().new(user)
        DBStorage().save()

    login_user(user)

    return redirect(url_for("core_view.home"))
