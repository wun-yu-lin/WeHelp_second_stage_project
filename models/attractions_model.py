import mysql.connector
import sys
sys.path.insert(1, './')
import config
import errorhandling.errorhandling as errorhandling


db_fig ={
    'host':config.MYSQL_HOST,
    'user':config.MYSQL_USER,
    'password':config.MYSQL_PASSWORD,
    'database':config.MYSQL_DATABASE,
    "pool_name":"mysql_pool",
    "pool_size":config.MYSQL_POOL_SIZE
}

def filter_query_string(query_string_arr)->bool:
    sql_filter_arr = config.SQL_FILTER_STRING

    for item in query_string_arr:
        for spec in sql_filter_arr: 
            if item == None: continue
            if item.find(spec)!=-1:
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

def get_attractions(keyword=None, page=1):
    
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)
    
    page = int(page)
    page_number =12
    data_start = (page-1)*12

    ##filter error query string
    if filter_query_string([keyword])==False: return errorhandling.handle_error({"code": 400, "message": "Invalid query string"}), 400

    ##non keyword search

    if keyword==None or keyword=="":
        mysql_str = "SELECT a.id, a.name, cat.category, a.description, a.address, a.transport, m.mrt, a.lat, a.lng, GROUP_CONCAT(DISTINCT img.src SEPARATOR ',') as images FROM attraction a LEFT JOIN attraction_info a_info on a.id = a_info.attraction_id LEFT JOIN mrt m on a.mrt_id = m.mrt_id LEFT JOIN category cat on a.category_id = cat.category_id LEFT JOIN image img on a.id = img.attraction_id GROUP BY a.id LIMIT %s,%s"
        cursor.execute(mysql_str, (data_start,page_number))
    else:
        mysql_str = "SELECT a.id, a.name, cat.category, a.description, a.address, a.transport, m.mrt, a.lat, a.lng, GROUP_CONCAT(DISTINCT img.src SEPARATOR ',') as images FROM attraction a LEFT JOIN attraction_info a_info on a.id = a_info.attraction_id LEFT JOIN mrt m on a.mrt_id = m.mrt_id LEFT JOIN category cat on a.category_id = cat.category_id LEFT JOIN image img on a.id = img.attraction_id WHERE (a.name LIKE %s or m.mrt LIKE %s ) GROUP BY a.id LIMIT %s,%s"
        query_str_partil = "%"+keyword+"%"
        query_str_compelete = keyword

 
        cursor.execute(mysql_str, (query_str_partil, query_str_compelete, data_start,page_number))
    try:
        
        results = cursor.fetchall()
        print("get attractions by keyword success!")

        pointer = 0
        for item in results:
            results[pointer]["images"] = item["images"].split(",")
            pointer+=1

        return results
    except Exception as err:
        print(err)
    finally:
        cursor.close()
        mysql_connection.close()


def get_attractions_by_id(id=1):

    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)


    mysql_str =  "SELECT a.id, a.name, cat.category, a.description, a.address, a.transport, m.mrt, a.lat, a.lng, GROUP_CONCAT(DISTINCT img.src SEPARATOR ',') as images FROM attraction a LEFT JOIN attraction_info a_info on a.id = a_info.attraction_id LEFT JOIN mrt m on a.mrt_id = m.mrt_id LEFT JOIN category cat on a.category_id = cat.category_id LEFT JOIN image img on a.id = img.attraction_id WHERE a.id = %s GROUP BY a.id"

    try:
        cursor.execute(mysql_str, (id,))
        results = cursor.fetchone()
        results["images"] = results["images"].split(",")

        return results
    except Exception as err:
        print(err)
        return errorhandling.handle_error({"code": 400, "message": "Server error"}), 400
