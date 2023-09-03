#!/usr/bin/python3

import os

from decouple import config
from flask import Flask, current_app, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """Create a Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config("APP_SETTINGS"))

    # ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    login_manager.refresh_view = "accounts_view.login"
    login_manager.login_view = "accounts_view.login"
    login_manager.login_message = "Login required."
    login_manager.needs_refresh_message = (
        "Please refresh your session before continuing"
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    CORS(
        app,
        resources={
            r"*": {"origins": ["http://127.0.0.1", "http://localhost"]}
        },
    )

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.alternative_id == user_id).first()

    from app.views import accounts_view
    from app.views import core_view

    app.register_blueprint(accounts_view)
    app.register_blueprint(core_view)
    app.add_url_rule("/", endpoint="accounts_view.home")

    return app
