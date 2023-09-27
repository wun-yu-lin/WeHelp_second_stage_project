from flask import request, jsonify,Response
import flask
# import sys
# sys.path.insert(1, './')
from errorhandling.errorhandling import handle_error
from controllers.user_controller import auth_signin_status
from models import booking_model
from http import HTTPStatus


##get booking info 
def get_booking() -> Response:
    if request.headers.get("Content-Type")!="application/json":
        return handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid request content type"})
    jwt_token = request.authorization.token
    auth_result = auth_signin_status(jwt_token)

    ##get booking info
    try:
        query_results = booking_model.get_unpayment_booking_by_userID(userID=auth_result["data"]["id"])
        if type(query_results) is flask.wrappers.Response:
            return query_results
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
                    "price": item["price"],
                    "booking_id": item["id"]
                }
            )
    except Exception as err:
        print(err)
        return handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "伺服器內部錯誤"})

    return jsonify({"data":data_result}), HTTPStatus.OK

##post booking info
def post_booking() -> Response: 

    ##check request content type
    if request.headers.get("Content-Type")!="application/json":
        return handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid request content type"})
    
    jwt_token = request.authorization.token
    auth_result = auth_signin_status(jwt_token)
    
    try:
        ##get request data
        request_data = request.get_json()
        print(request_data)

        ##確認是否已經有相同的booking on same attraction id and date and time, 如有則修改原先訂單為取消
        query_results = booking_model.get_unpayment_booking_by_userID_and_attraction_id_date_time(
            userID=auth_result["data"]["id"],
            attraction_id=request_data["attractionId"],
            date=request_data["date"],
            time=request_data["time"]
            )
        if query_results is not []:
            for item in query_results:
                update_results = booking_model.change_booking_order_status_to_cancel_and_check_user_id(booking_id=item["id"], user_id=auth_result["data"]["id"])
        

        ##insert data into database
        post_results=booking_model.post_booking_into_database(
            user_id=int(auth_result["data"]["id"]), 
            attraction_id=int(request_data["attractionId"]), 
            date=str(request_data["date"]), 
            time=str(request_data["time"]), 
            price=int(request_data["price"])
            )
    except Exception as err:
        print(err)
        return handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "伺服器內部錯誤"})
    ##error handling
    if type(post_results) is flask.Response:
        return post_results
    
    return jsonify({"ok":True}), HTTPStatus.OK

##delete booking info
def delete_booking() -> Response:
    if request.headers.get("Content-Type")!="application/json":
        return handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid request content type"})
    jwt_token = request.authorization.token
    auth_result = auth_signin_status(jwt_token)
    request_booking_id_arr = request.get_json()["booking_id"]
    user_id = auth_result["data"]["id"]
    
    ##change booking order status 1 to 0 (cancel)
    for item in request_booking_id_arr:
        try:
            delete_results = booking_model.change_booking_order_status_to_cancel_and_check_user_id(booking_id=item, user_id=user_id)
        except Exception as err:
            print(err)
            return handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "伺服器內部錯誤"})
        
        ##error handling
        if type(delete_results) is flask.wrappers.Response:
            return delete_results
    
    

    return jsonify({"ok":True}), HTTPStatus.OK

