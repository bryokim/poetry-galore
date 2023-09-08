from flask import Blueprint, make_response, jsonify

core_view = Blueprint("core_view", __name__)
api_view = Blueprint("api_view", __name__, url_prefix="/api/v1")

from .register import *
from .login import *
from .home import *

from .users import *
from .poems import *
from .poems_likes import *
from .comments import *
from .categories import *
from .themes import *

from .api import *


@core_view.errorhandler(404)
def handle_404(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@core_view.errorhandler(400)
def handle_400(error):
    return make_response(jsonify({"error": error.description}), 400)
