from flask import jsonify,request,Response
import flask
import errorhandling.errorhandling as errorhandling
import models.user_model as user_model
import hashlib
import jwt
import config 
import datetime 
from http import HTTPStatus

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



##註冊會員帳戶
def post_user():
    try:
        request_object = request.get_json()
    except Exception as err:
        print(err)
        return
    if request.headers["content-type"]!="application/json": return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid request content type"})


    ##hash password
    request_object["password"] = hash_password(request_object["password"])

    ##check user alraedy exists or not
    check_results  = user_model.get_user_data_by_email(email=request_object["email"])
    print(type(check_results))
    if type(check_results) is flask.wrappers.Response:
        return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "請輸入正確的email格式, 不能有空白或是特殊符號"})
    if check_results != [] :
        return errorhandling.handle_error({"code": HTTPStatus.NOT_FOUND, "message": "Email already signup!"})

    ##insert user data
    try:
        insert_id= user_model.insert_user_data_into_user_table(name=request_object["name"],
                                                    email=request_object["email"],
                                                    password=request_object["password"])
        print(insert_id)
    except:
        return errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "Internal database server error"})
                                            
    
    return  jsonify({"ok":True}), HTTPStatus.CREATED
    
##取得會員資料 需要ＪＷＴ認證
def get_user_auth():
    request_bearer_token = request.headers["Authorization"]
    if request_bearer_token == None: return jsonify(None), HTTPStatus.FORBIDDEN
    try:
        request_bearer_token = request_bearer_token.split("Bearer ")[1]
        decode = jwt.decode(jwt=request_bearer_token, 
                            key = config.HS256_KEY, 
                            audience=request.host_url,
                            algorithms=['HS256'],
                            issuer='example.com',
                            options={"verify_exp":True})

        return jsonify({"data":{"id":decode["id"], "name":decode["name"], "email":decode["email"]}}), HTTPStatus.OK
    except Exception as err:
        print(err)
        return jsonify(None), HTTPStatus.FORBIDDEN
    
##登入會員帳戶
def put_user_auth():
    try:
        request_object = request.get_json()
    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid request body"})
    if request.headers["content-type"]!="application/json": return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid request content type"})

    ##hash password
    request_object["password"] = hash_password(request_object["password"])

    try:
        query_results = user_model.get_user_data_by_email_password(request_object["email"],request_object["password"])
        print(query_results)
        if type(query_results) is flask.wrappers.Response or type(query_results) is Response:
            return query_results
        if query_results == []:
            return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid email or password, login fialed"})

    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "Internal database erver error"})

    ##create jwt token
    try:

        payload = {
                'iss': 'example.com', ## (Issuer) Token 的發行者
                'sub':  str(request_object["email"]), ## (Subject) 也就是使用該 Token 的使用者
                'aud':  str(request.host_url), #(Audience) Token 的接收者，也就是後端伺服器
                'exp': datetime.datetime.now() + datetime.timedelta(days=7),  #(Expiration Time) Token 的過期時間
                'id': query_results[0]["id"],
                "email" : query_results[0]["email"],
                "name" : query_results[0]["name"]
                }

        token = jwt.encode(payload, config.HS256_KEY, algorithm='HS256')
    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "Internal server error"})
    
    

    return jsonify({"token":token}), HTTPStatus.OK


