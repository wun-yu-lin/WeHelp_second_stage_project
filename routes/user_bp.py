from flask import Blueprint
import controllers.user_controller as user_controller

blueprints = Blueprint('user_bp', __name__, url_prefix='/api/user')

blueprints.route("/", methods=["POST"])(user_controller.post_user)
blueprints.route("/auth", methods=["GET"])(user_controller.get_user_auth)
blueprints.route("/auth", methods=["PUT"])(user_controller.put_user_auth)
