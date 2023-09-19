from flask import jsonify,request
import errorhandling.errorhandling as errorhandling
import models.user_model as user_model
import hashlib
import jwt
import config 
import datetime 

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



##註冊會員帳戶
def post_user():
    try:
        request_object = request.get_json()
    except Exception as err:
        print(err)
        return
    if request.headers["content-type"]!="application/json": return errorhandling.handle_error({"code": 400, "message": "Invalid request content type"})


    ##hash password
    request_object["password"] = hash_password(request_object["password"])

    ##check user alraedy exists or not
    check_results  = user_model.get_user_data_by_email(email=request_object["email"])

    if check_results != [] :
        return errorhandling.handle_error({"code": 404, "message": "Account already signup or erorr user data"})

    ##insert user data
    try:
        insert_id= user_model.insert_user_data_into_user_table(name=request_object["name"],
                                                    email=request_object["email"],
                                                    password=request_object["password"])
        print(insert_id)
    except:
        return errorhandling.handle_error({"code": 500, "message": "Internal database server error"})
                                            
    
    return  jsonify({"ok":True}), 201
    
##取得會員資料 需要ＪＷＴ認證
def get_user_auth():
    request_bearer_token = request.headers["Authorization"]
    if request_bearer_token == None: return jsonify(None), 403
    try:
        request_bearer_token = request_bearer_token.split("Bearer ")[1]
        decode = jwt.decode(jwt=request_bearer_token, 
                            key = config.HS256_KEY, 
                            audience=request.host_url,
                            algorithms=['HS256'],
                            issuer='example.com',
                            options={"verify_exp":True})

        return jsonify({"data":{"id":decode["id"], "name":decode["name"], "email":decode["email"]}}), 200
    except Exception as err:
        print(err)
        return jsonify(None), 400
    
##登入會員帳戶
def put_user_auth():
    try:
        request_object = request.get_json()
    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": 400, "message": "Invalid request body"})
    if request.headers["content-type"]!="application/json": return errorhandling.handle_error({"code": 400, "message": "Invalid request content type"})

    ##hash password
    request_object["password"] = hash_password(request_object["password"])

    try:
        query_results = user_model.get_user_data_by_email_password(request_object["email"],request_object["password"])
        if query_results == []:
            return errorhandling.handle_error({"code": 400, "message": "Invalid email or password, login fialed"})

    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": 500, "message": "Internal database erver error"})

    ##create jwt token
    try:
        exp_time_int = int(round((datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()))
        payload = {
                'iss': 'example.com', ## (Issuer) Token 的發行者
                'sub':  str(request_object["email"]), ## (Subject) 也就是使用該 Token 的使用者
                'aud':  str(request.host_url), #(Audience) Token 的接收者，也就是後端伺服器
                'exp': str(exp_time_int),  #(Expiration Time) Token 的過期時間
                'id': query_results[0]["id"],
                "email" : query_results[0]["email"],
                "name" : query_results[0]["name"]
                }

        token = jwt.encode(payload, config.HS256_KEY, algorithm='HS256')
    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": 500, "message": "Internal server error"}), 500
    
    

    return jsonify({"token":token}), 200