from flask import Blueprint
from controllers.attractions_controller import *

blueprints = Blueprint("attractions", __name__, url_prefix="/api/attractions")

blueprints.route("/", methods=["GET"])(get_attractions)
blueprints.route("/<int:attractionId>", methods=["GET"])(get_attraction_by_id)