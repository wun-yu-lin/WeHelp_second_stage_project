import mysql.connector
import sys
sys.path.insert(1, './')
import config
import errorhandling.errorhandling as errorhandling
from http import HTTPStatus

db_fig ={
    'host':config.MYSQL_HOST,
    'user':config.MYSQL_USER,
    'password':config.MYSQL_PASSWORD,
    'database':config.MYSQL_DATABASE,
    "pool_name":"booking_pool",
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


def get_unpayment_booking_by_userID_and_attraction_id_date_time(userID:int, attraction_id:int, date:str, time:str):
    ##filter error query string
    if filter_query_string([userID])==False: return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid query string"})

    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)
    cursor.execute("SET SESSION group_concat_max_len = %s", (config.GROUP_CONCAT_MAX_LEN,))

    mysql_str = "SELECT i.attraction_id, b.id , a.name, a.address, b.date,b.time, b.price, GROUP_CONCAT(DISTINCT i.src SEPARATOR ',') as images FROM taipei_travel.user u left join taipei_travel.booking b on u.id = b.user_id left join taipei_travel.attraction a on a.id = b.attraction_id left join taipei_travel.image i on a.id = i.attraction_id where u.id = %s AND b.booking_status = 1 and a.id = %s and b.date=%s and b.time=%s group by b.id;"
 
    try:
        
        cursor.execute(mysql_str, (userID,attraction_id,date,time,))
        results = cursor.fetchall()
        print("get booking by user_id success!")
        mysql_connection.commit()

 
    except Exception as err:
        print(err)
        results = errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "MySQL Server error"})

    finally:
        cursor.close()
        mysql_connection.close()

    return results



def get_unpayment_booking_by_userID(userID:int):
    ##filter error query string
    if filter_query_string([userID])==False: return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid query string"})

    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)
    
    cursor.execute("SET SESSION group_concat_max_len = %s", (config.GROUP_CONCAT_MAX_LEN,))

    mysql_str = "SELECT i.attraction_id, b.id , a.name, a.address, b.date,b.time, b.price, GROUP_CONCAT(DISTINCT i.src SEPARATOR ',') as images FROM taipei_travel.user u left join taipei_travel.booking b on u.id = b.user_id left join taipei_travel.attraction a on a.id = b.attraction_id left join taipei_travel.image i on a.id = i.attraction_id where u.id = %s AND b.booking_status = 1 group by b.id;"
 
    try:
        
        cursor.execute(mysql_str, (userID,))
        results = cursor.fetchall()
        print("get booking by user_id success!")
        mysql_connection.commit()

 
    except Exception as err:
        print(err)
        results = errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "MySQL Server error"})

    finally:
        cursor.close()
        mysql_connection.close()

    return results



def post_booking_into_database(user_id:int, attraction_id:int, date:str, time:str, price:int,):

    # ##filter error query string
    if filter_query_string([user_id, attraction_id, date])==False: return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, "message": "Invalid query string"})
    
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)

    mysql_str = "INSERT INTO taipei_travel.booking (date, time, price, booking_status, user_id, attraction_id) values (%s,%s, %s, %s, %s, %s);"

 
    try:
        cursor.execute(mysql_str, (date, time, price, 1, user_id, attraction_id))
        #get booking id
        results = str(cursor.lastrowid)
        mysql_connection.commit()
        print("get booking by user_id success!")
        

 
    except Exception as err:
        print(err)
        results = errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "MySQL Server error"})

    finally:
        cursor.close()
        mysql_connection.close()

    return results



def change_booking_order_status_to_cancel_and_check_user_id(booking_id:int, user_id:int):
    # ##filter error query string
    if filter_query_string([booking_id])==False: return errorhandling.handle_error({"code": HTTPStatus.BAD_REQUEST, 
    "message": "Invalid query string"})
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)

    mysql_str = "UPDATE taipei_travel.booking SET booking_status=0 where id = %s and user_id= %s;"

    try:
        cursor.execute(mysql_str, (booking_id, user_id))
        #get booking id
        results = cursor.lastrowid
        mysql_connection.commit()
        print("get booking by user_id success!")
 
    except Exception as err:
        print(err)
        results = errorhandling.handle_error({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "MySQL Server error"})

    finally:
        cursor.close()
        mysql_connection.close()

    return results
