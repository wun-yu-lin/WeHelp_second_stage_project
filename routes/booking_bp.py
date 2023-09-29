from flask import Blueprint,request
from errorhandling.errorhandling import handle_error
from controllers.booking_controller import *
from controllers.user_controller import auth_signin_status
blueprints = Blueprint("booking", __name__, url_prefix="/api/booking")

def booking_before_auth():
    try:
        jwt_token = request.authorization.token
        auth_result = auth_signin_status(jwt_token)
        if auth_result["data"] == None:
            return handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "請先登入會員"})
    except Exception as err:
        print(err)
        return handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "請先登入會員"})
    
blueprints.before_request(booking_before_auth)




blueprints.route("/", methods=["GET"])(get_booking)
blueprints.route("/", methods=["POST"])(post_booking)
blueprints.route("/", methods=["DELETE"])(delete_booking)