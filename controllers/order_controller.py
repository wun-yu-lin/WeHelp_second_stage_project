from flask import jsonify,request,Response
import flask, json, requests
import errorhandling.errorhandling as errorhandling
import models.user_model as user_model
import models.order_model  as order_model
import config 
from http import HTTPStatus
from flask import make_response
from controllers.user_controller import auth_signin_status

TAPPAY_PARTNER_KEY = config.TAPPAY_PARTNER_KEY
TAPPAY_DIRECT_PAY_URL = config.TAPPAY_DIRECT_PAY_URL





##建立新的訂單，並完成付程序
## ./api/orders with post method
def post_orders():

    ##解密jwt token 取得使用者資訊
    auth_result = auth_signin_status(request.authorization.token)
    if auth_result['data'] == None: return errorhandling.handle_error({"code": HTTPStatus.UNAUTHORIZED, "message": "Unauthorized"}) 
    if request.headers["content-type"] != "application/json": return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Bad Request"})

    try:
        ##取得前端傳送的資訊
        request_data = request.get_json()
        print("request_data",request_data)

        ##save order to database return order id
        ##1. 新增訂單資訊到 taipei_travel.order, 狀態為未付款
        ##2. 更新order id 到相對應的 booking tabel, 並修改 booking 狀態為未booking
        save_order_results = order_model.save_unpayed_order_into_order_tabel_and_change_orderID_in_booking_table(
            user_id=int(auth_result['data']['id']),
            order_object=request_data
        )
            ##如server端有錯誤，直接回傳錯誤訊息
        if type(save_order_results) == flask.wrappers.Response: return save_order_results



        ##call tappay api with dircet pay method
        ord_request_header = {
            "content-type": "application/json",
            "x-api-key": config.TAPPAY_PARTNER_KEY,
        }
        ord_request_data = {
            ## "card_key": String, 
            ## "card_token": String,
            "details":"TapPay Test for Taipei travel project",
            "amount": request_data["order"]["price"],
            "prime": request_data["prime"],
            "partner_key": config.TAPPAY_PARTNER_KEY,
            "merchant_id": config.TAPPAY_DIRECT_PAY_MERCHNAT_ID,
            "currency": "TWD",
            "amount": request_data["order"]["price"],
            "cardholder": {
                "phone_number": request_data["order"]["contact"]["phone"],
                "name": request_data["order"]["contact"]["name"],
                "email": request_data["order"]["contact"]["email"],
            },
            "remember": False
        }
        ##requst to TapPay API
        response_data = requests.post(
            url=config.TAPPAY_DIRECT_PAY_URL,
            headers=ord_request_header,
            data=json.dumps(ord_request_data),
            ).json()
        print("response_data",response_data)


        ##判斷是否成功，按照付款結果，更新訂單狀態 in database taipei_travel.order
        if response_data["status"]==0:
            print("交易成功")
            ##交易成功      
            update_results = order_model.update_order_status_and_number(
                user_id=int(auth_result['data']['id']),
                order_id=int(save_order_results),
                status_code=1,
                number=response_data["bank_transaction_id"])
            print("update_results",update_results)

            ##prepare response data to client
            response_to_client_data = {
                "numbet":response_data["bank_transaction_id"],
                "payment": {
                    "status": 0,
                    "message": "付款成功"
                }
            }

            return jsonify({"data":response_to_client_data})
        else:
            ##交易失敗
            update_results = order_model.update_order_status_and_number(
                userID=int(auth_result['data']['id']),
                order_id=str(save_order_results),
                status_code=2,
                number=0
            )
            return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": response_data["msg"]})



        

    except Exception as e: 
        print("error",e)
        return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Bad Request"})
    

    return "post_orders"

##根據訂單編號取得訂單資訊
## ./api/order
def get_order_by_order_number(order_number:int):
    return "get_order_by_order_number" + str(order_number)