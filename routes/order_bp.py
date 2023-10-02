from flask import Blueprint,request
from errorhandling.errorhandling import handle_error
from controllers.order_controller import *
from controllers.user_controller import auth_signin_status
from http import HTTPStatus
blueprints_orders = Blueprint("orders", __name__, url_prefix="/api/orders")
blueprints_order = Blueprint("order", __name__, url_prefix="/api/order")

def order_before_auth():
    try:
        jwt_token = request.authorization.token
        auth_result = auth_signin_status(jwt_token)
        if auth_result["data"] == None:
            return handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "請先登入會員"})
    except Exception as err:
        print(err)
        return handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "請先登入會員"})
    
blueprints_orders.before_request(order_before_auth)
blueprints_order.before_request(order_before_auth)


blueprints_orders.route("/", methods=["POST"])(post_orders) ####建立新的訂單，並完成付程序
blueprints_order.route("/<int:order_number>", methods=["GET"])(get_order_by_order_number) ##根據訂單編號取得訂單資訊