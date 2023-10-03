import mysql.connector
import config
import errorhandling.errorhandling as errorhandling
from http import HTTPStatus

db_fig ={
    'host':config.MYSQL_HOST,
    'user':config.MYSQL_USER,
    'password':config.MYSQL_PASSWORD,
    'database':config.MYSQL_DATABASE,
    "pool_name":"order_pool",
    "pool_size":config.MYSQL_POOL_SIZE
}


query_config = {
    "group_concat_max_len":config.GROUP_CONCAT_MAX_LEN
}

def filter_query_string(query_string_arr)->bool:
    sql_filter_arr = config.SQL_FILTER_STRING

    for item in query_string_arr:
        item = str(item)
        for spec in sql_filter_arr: 
            if item == None: continue
            if item.upper().find(spec.upper())!=-1:
                return False 
    return True

    

##mysql connection pool
try:
    mysql_connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db_fig)
    print("create mysql connection success!")

except Exception as err:
    print(err)
    print("create mysql connection error!")

def get_mysql_connection_from_pool(mysql_connection_pool):
    mysql_connection = mysql_connection_pool.get_connection()
    print("get mysql connection success!")
    return mysql_connection

##此function 需要修改喔！！booking and order 在同一個 transaction
def save_unpayed_order_into_order_tabel_and_change_orderID_in_booking_table(user_id:int, order_object:dict)-> str:
    '''
    ##save order to database return order id
    ##1. 新增訂單資訊到 taipei_travel.order, 狀態為未付款
    ##2. 更新order id 到相對應的 booking tabel, 並修改 booking 狀態為未booking
    save order info into database, return order id, if error rollback return response from errorhandling

    order_object
    {
        "prime": "前端從第三方金流 TapPay 取得的交易碼",
        "order": {
            "price": 2000, 
            "booking_id": [1,2,3,4,5,6,7]
            "trip": [
                {
                "attraction": {
                    "id": 10,
                    "name": "平安鐘",
                    "address": "臺北市大安區忠孝東路 4 段",
                    "image": "https://yourdomain.com/images/attraction/10.jpg"
                },
                "date": "2022-01-31",
                "time": "afternoon"
                }
            ]
            ,
            "contact": {
                "name": "彭彭彭",
                "email": "ply@ply.com",
                "phone": "0912345678"
            }
        }
    }
    '''
    booking_id_arr = order_object["order"]["booking_id"]
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)

    order_mysql_str = "Insert into taipei_travel.order (order_price, prime, status, number, contact_name, contact_email, contact_phone, user_id) values (%s, %s, %s, %s,%s, %s, %s, %s);"
    booking_mysql_str = "UPDATE taipei_travel.booking SET booking_status= 1,order_id = %s where id = %s and user_id= %s;"
 
    try:
        
        cursor.execute(order_mysql_str, (
                                float(order_object["order"]["price"]),
                                str(order_object["prime"]),
                                int(1),
                                int(0),
                                str(order_object["order"]["contact"]["name"]),
                                str(order_object["order"]["contact"]["email"]),
                                str(order_object["order"]["contact"]["phone"]),
                                int(user_id), 
                                ))
        order_id=cursor.lastrowid
        print("order_id",order_id)
        results = order_id
        for booking_id in booking_id_arr:
            cursor.execute(booking_mysql_str, (
                                int(order_id),
                                int(booking_id),
                                int(user_id), 
                                ))
            print("booking_id",booking_id)
            print("ord_id",order_id)
            print("user_id",user_id)


        ##finish transaction and commit
        mysql_connection.commit()
        print("insert order, change order_id in booking tabel success!")

 
    except Exception as err:
        print(err)
        results = errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "MySQL Server error"})
        mysql_connection.rollback()

    finally:
        cursor.close()
        mysql_connection.close()

    return results


def update_order_status_and_number(user_id:int,order_id:int,status_code:int,number:str)-> str:
    '''
    This function is used to update order status and number,
    if success return updated order id 
    if error return response from errorhandling
    status code (
        0:payed
        1:unpay
        2:failed pay or cancel
        )
    '''
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)

    mysql_str = "UPDATE taipei_travel.order SET status = %s where id = %s and user_id = %s;"
 
    try:
        
        cursor.execute(mysql_str, (
                                int(status_code),
                                int(order_id),
                                int(user_id), 
                                ))
        results=cursor.lastrowid
        mysql_connection.commit()
        
        print("update order success!")

 
    except Exception as err:
        print(err)
        results = errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "MySQL Server error"})

    finally:
        cursor.close()
        mysql_connection.close()

    return results