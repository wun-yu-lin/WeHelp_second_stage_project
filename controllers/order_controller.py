from flask import jsonify,request,Response
import flask
import errorhandling.errorhandling as errorhandling
import models.user_model as user_model
import config 
from http import HTTPStatus
from flask import make_response

TAPPAY_PARTNER_KEY = config.TAPPAY_PARTNER_KEY
TAPPAY_DIRECT_PAY_URL = config.TAPPAY_DIRECT_PAY_URL





##建立新的訂單，並完成付程序
## ./api/orders
def post_orders():
    

    return "post_orders"

##根據訂單編號取得訂單資訊
## ./api/order
def get_order_by_order_number(order_number:int):
    return "get_order_by_order_number" + str(order_number)