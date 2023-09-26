from flask import Blueprint, request, jsonify, blueprints
import sys
sys.path.insert(1, './')
from errorhandling.errorhandling import handle_error
from controllers.user_controller import auth_signin_status

from models import booking_model,attractions_model
from http import HTTPStatus


##get booking info 
def get_booking():
    try:
        jwt_token = request.authorization.token
        auth_result = auth_signin_status(jwt_token)
        if auth_result["data"] == None:
            return handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "請先登入會員"})
    except Exception as err:
        print(err)
        return handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "請先登入會員"})
    ##get booking info
    try:
        query_results = booking_model.get_unpayment_booking_by_userID(userID=auth_result["data"]["id"])
        data_result = []
        for item in query_results:
            data_result.append(
                {
                    "attraction": {
                        "id": item["attraction_id"],
                        "name": item["name"],
                        "address": item["address"],
                        "image": item["images"].split(",")[0]
                    },
                    "date": item["date"],
                    "time": item["time"],
                    "price": item["price"]
                }
            )
    except Exception as err:
        print(err)
        return handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "伺服器內部錯誤"})

    return jsonify({"data":data_result}), HTTPStatus.OK

##post booking info
def post_booking():
    jwt_token = request.authorization.token
    auth_result = auth_signin_status(jwt_token)
    if auth_result["data"] == None:
        return handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "請先登入會員"})

    return "post_booking"


##delete booking info
def delete_booking():
    jwt_token = request.authorization.token
    auth_result = auth_signin_status(jwt_token)
    if auth_result["data"] == None:
        return handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "請先登入會員"})

    return "delete_booking"

