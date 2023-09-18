from flask import jsonify,request
import errorhandling.errorhandling as errorhandling
import models.user_model as user_model
import hashlib
import jwt


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



##註冊會員帳戶
def post_user():
    try:
        request_object = request.get_json()
    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": 400, "message": "Invalid request body"}), 400
    if request.headers["content-type"]!="application/json": return errorhandling.handle_error({"code": 400, "message": "Invalid request content type"}), 400

    ##hash password
    request_object["password"] = hash_password(request_object["password"])

    ##check user alraedy exists or not
    if user_model.get_user_data_by_email_password(email=request_object["email"],
                                                  password=request_object["password"]
                                                  ) != [] :
        return errorhandling.handle_error({"code": 400, "message": "Acccount already signup "}), 400

    ##insert user data
    try:
        insert_id= user_model.insert_user_data_into_user_table(name=request_object["name"],
                                                    email=request_object["email"],
                                                    password=request_object["password"])
        print(insert_id)
    except:
        return errorhandling.handle_error({"code": 500, "message": "Internal database erver error"}), 500
                                            
    
    return  jsonify({"ok":True}), 201
    
##取得會員資料 需要ＪＷＴ認證
def get_user_auth():

    
    return "get_user_auth"
    
##登入會員帳戶
def put_user_auth():

    
    

    return "put_user_auth"