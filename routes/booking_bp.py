from flask import Blueprint
from controllers.booking_controller import *
blueprints = Blueprint("booking", __name__, url_prefix="/api/booking")

blueprints.route("/", methods=["GET"])(get_booking)
blueprints.route("/", methods=["POST"])(post_booking)
blueprints.route("/", methods=["DELETE"])(delete_booking)