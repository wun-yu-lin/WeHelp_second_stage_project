from flask import Blueprint
from controllers.mrt_controller import *

blueprints = Blueprint("mrts", __name__, url_prefix="/api/mrts")

blueprints.route("/", methods=["GET"])(get_mrts)
