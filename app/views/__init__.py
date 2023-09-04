from flask import Blueprint, make_response, jsonify

accounts_view = Blueprint("accounts_view", __name__)
core_view = Blueprint("core_view", __name__, url_prefix="/api/v1")

from .register import *
from .login import *
from .home import *
from .settings import *

from .users import *
from .poems import *
from .poems_likes import *
from .comments import *
from .categories import *
from .themes import *
from .search import *


@core_view.errorhandler(404)
def handle_404(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@core_view.errorhandler(400)
def handle_400(error):
    return make_response(jsonify({"error": error.description}), 400)
