import json
import requests

from decouple import config
from flask import request, redirect, url_for
from flask_login import login_user
from oauthlib.oauth2 import WebApplicationClient

from app.models.user import User
from app.models.engine.db_storage import DBStorage


GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


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
