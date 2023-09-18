import mysql.connector
import sys

import config
import errorhandling.errorhandling as errorhandling
from flask import jsonify 


db_fig ={
    'host':config.MYSQL_HOST,
    'user':config.MYSQL_USER,
    'password':config.MYSQL_PASSWORD,
    'database':config.MYSQL_DATABASE,
    "pool_name":"mrts_pool",
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

def get_mrt_data():
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)

    mysql_str = "SELECT m.mrt from attraction a LEFT JOIN mrt m on a.mrt_id = m.mrt_id GROUP BY (m.mrt) Order by count(m.mrt) desc"

    try:
        cursor.execute(mysql_str)
        res_data = cursor.fetchall()
        resutls_arr= []
        for item in res_data:
            resutls_arr.append(item["mrt"])
    except Exception as err:
        print(err)
        resutls_arr = jsonify({"error": True, "message": "Server error"})
    finally:
        cursor.close()
        mysql_connection.close()
    return resutls_arr
    
