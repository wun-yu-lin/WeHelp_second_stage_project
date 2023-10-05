from flask import jsonify,request
from flask.wrappers import Response
import flask, json, requests
import errorhandling.errorhandling as errorhandling
import models.order_model  as order_model
import models.booking_model as booking_model
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

        ##驗證前端送來的價格資料是否正確
        booking_id_arr = request_data["order"]["booking_id_arr"]
        request_total_price = int(request_data["order"]["price"])
        calculate_total_price = int(booking_model.calculate_total_price(booking_id_arr))
        if request_total_price != calculate_total_price: return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "駭客不要串改價格，小本生意而已～ 放下屠刀，立地成佛"})
        

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

        ##判斷是否成功，按照付款結果，更新訂單狀態 in database taipei_travel.order
        if response_data["status"]==0:
            print("交易成功")
            ##交易成功      
            update_results = order_model.update_order_status_and_number(
                user_id=int(auth_result['data']['id']),
                order_id=int(save_order_results),
                status_code=0,
                number=response_data["rec_trade_id"])

            ##prepare response data to client
            response_to_client_data = {
                "number":response_data["rec_trade_id"],
                "payment": {
                    "status": 0,
                    "message": "付款成功"
                }
            }

            return jsonify({"data":response_to_client_data})
        else:
            ##交易失敗
            print("交易失敗")
            update_results = order_model.update_order_status_and_number(
                user_id=int(auth_result['data']['id']),
                order_id=str(save_order_results),
                status_code=2,
                number=0
            )
            return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": response_data["msg"]})



        

    except Exception as e: 
        print("error",e)
        return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Bad Request"})
    


##根據訂單編號取得訂單資訊
## ./api/order
def get_order_by_order_number() -> Response:
    try:
        order_number = request.args.get("number")
        ##check input data type
        if type(order_number) != str: return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Bad Request"})

        ##解密jwt token 取得使用者資訊
        auth_result = auth_signin_status(request.authorization.token)
        
        #get orderdata from database
        query_data = order_model.get_order_info_by_order_number(
            user_id=int(auth_result['data']['id']),
            order_number=str(order_number)
        )
        ##if not data
        if query_data[0] == None: return jsonify({"data":None})

        print("query_data",query_data)
        

        trip_arr = []
        for item in query_data:
            trip_arr.append(
                {
                    "attraction": {
                        "id": item["attraction_id"],
                        "name": item["attraction_name"],
                        "address": item["address"],
                        "image": item["image_src"]
                    },
                    "date": item["date"],
                    "time": item["time"]   
                }
            )

        order_data = {
            "number": query_data[0]["number"],
            "price": int(query_data[0]["order_price"]),
            "trip": trip_arr,
            "contact": {
                "name": query_data[0]["contact_name"],
                "email": query_data[0]["contact_email"],
                "phone": query_data[0]["contact_phone"]
            },
            "status": int(query_data[0]["status"])
        }
    except Exception as e:
        print("error",e)
        return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Bad Request"})



    return jsonify({"data":order_data})