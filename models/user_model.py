import mysql.connector
import config
import errorhandling.errorhandling as errorhandling
from flask import jsonify 


db_fig ={
    'host':config.MYSQL_HOST,
    'user':config.MYSQL_USER,
    'password':config.MYSQL_PASSWORD,
    'database':config.MYSQL_DATABASE,
    "pool_name":"user_pool",
    "pool_size":config.MYSQL_POOL_SIZE
}

def filter_query_string(query_string_arr)->bool:
    sql_filter_arr = config.SQL_FILTER_STRING

    for item in query_string_arr:
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

def get_user_data_by_email_password(email,password):
    
    try:
        email = str(email)
        password = str(password)
    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": 400, "message": "Invalid query string"}), 400
    if filter_query_string([email,password])==False: return errorhandling.handle_error({"code": 400, "message": "Invalid query string"}), 400
    try:
        mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
        cursor = mysql_connection.cursor(dictionary=True)

        mysql_str = "SELECT u.id, u.name, u.email FROM user u WHERE email = %s AND password = %s"
        cursor.execute(mysql_str,(email,password,))
        cursor_result = cursor.fetchall()
        mysql_connection.commit()

    except Exception as err:
        print(err)

    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
        cursor.close()
        mysql_connection.close()

    return cursor_result

def get_user_data_by_name_email(name,email):
    try:
        email = str(email)
        name = str(name)
    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": 400, "message": "Invalid query string"}), 400
    if filter_query_string([name,email])==False: return errorhandling.handle_error({"code": 400, "message": "Invalid query string"}), 400
    try:
        mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
        cursor = mysql_connection.cursor(dictionary=True)

        mysql_str = "SELECT u.id, u.name, u.email FROM user u WHERE name = %s AND email = %s"
        cursor.execute(mysql_str,(name,email,))
        cursor_result = cursor.fetchall()
        mysql_connection.commit()

    except Exception as err:
        print(err)

    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
            mysql_connection.close()
        cursor.close()
        mysql_connection.close()

    return cursor_result, 200


def insert_user_data_into_user_table(name, email, password):
   
    try:
        name = str(name)
        email = str(email)
        password = str(password)

    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": 400, "message": "Invalid query string"}), 400
    if filter_query_string([name,email,password])==False: return errorhandling.handle_error({"code": 400, "message": "Invalid query string"}), 400


    try:
        mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
        cursor = mysql_connection.cursor(dictionary=True)

        mysql_str = "insert into user (name, email, password) values (%s,%s,%s)"
        cursor.execute(mysql_str,(name,email,password,))
        insert_id = cursor.lastrowid
        mysql_connection.commit()

    except Exception as err:
        print(err)

    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
            mysql_connection.close()
        cursor.close()
        mysql_connection.close()

    return insert_id