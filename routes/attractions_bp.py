from flask import Blueprint
from controllers.attractions_controller import *

blueprints_v1 = Blueprint("attractions", __name__, url_prefix="/api/attractions")
blueprints_v2 = Blueprint("attraction", __name__, url_prefix="/api/attraction")
blueprints_v1.route("/", methods=["GET"])(get_attractions)
blueprints_v2.route("/<int:attractionId>", methods=["GET"])(get_attraction_by_id)