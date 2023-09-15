import mysql.connector
import sys
sys.path.insert(1, './')
import config

# import subprocess
# ##control groupconcat string limit in mySQL
# subprocess.call("ps aux",shell=True)

db_fig ={
    'host':config.MYSQL_HOST,
    'user':config.MYSQL_USER,
    'password':config.MYSQL_PASSWORD,
    'database':config.MYSQL_DATABASE,
    "pool_name":"mysql_pool",
    "pool_size":10
}

query_config = {
    "group_concat_max_len":config.GROUP_CONCAT_MAX_LEN
}

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



def insert_mrt_data_into_taipei_travel(mrt):
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor()
    mysql_str = "INSERT INTO mrt(mrt) VALUES (%s)"
    try:
        cursor.execute(mysql_str, (str(mrt),))
        mysql_connection.commit()
        print("insert mrt data  success!")
    except Exception as err:
        print(err)
        mysql_connection.rollback()
    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
        cursor.close()
        mysql_connection.close()
def insert_category_data_into_taipei_travel(category):
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor()
    mysql_str = "INSERT INTO category(category) VALUES (%s)"
    try:
        cursor.execute(mysql_str, (str(category),))
        mysql_connection.commit()
        print("insert category data success!")
    except Exception as err:
        print(err)
        mysql_connection.rollback()
    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
        cursor.close()
        mysql_connection.close()


def get_all_mrt_data_from_taipei_travel():
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)
    mysql_str = "select * from mrt"
    try:
        cursor.execute(mysql_str)
        collection = cursor.fetchall()
        mysql_connection.commit()
        return collection
    except Exception as err:
        print(err)
        mysql_connection.rollback()
        return None
    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
        cursor.close()
        mysql_connection.close()

def get_all_category_data_from_taipei_travel():
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)
    mysql_str = "select * from category"
    try:
        cursor.execute(mysql_str)
        collection = cursor.fetchall()
        mysql_connection.commit()
        return collection
    except Exception as err:
        print(err)
        mysql_connection.rollback()
        return None
    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
        cursor.close()
        mysql_connection.close()

def insert_into_attraction(attraction_object):

    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)
    mysql_str = "INSERT INTO attraction(address, category_id, description, lat, lng, mrt_id, name, transport, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(mysql_str, 
                       (attraction_object["address"],
                        attraction_object["category_id"],
                        attraction_object["description"],
                        attraction_object["lat"],
                        attraction_object["lng"],
                        attraction_object["mrt_id"],
                        attraction_object["name"],
                        attraction_object["transport"],
                        attraction_object["attraction_id"])
                       )
        mysql_connection.commit()
        print("insert attraction data success!")
    except Exception as err:
        print("error in insert_into_attraction")
        print(err)
    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
        cursor.close()
        mysql_connection.close()

def insert_attraction_info(attraction_object):
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)
    mysql_str = "INSERT INTO attraction_info(attraction_id, av_begin, av_end, idpt, memo_time, poi, rate, ref_wp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        cursor.execute(mysql_str, 
                       (attraction_object["attraction_id"],
                        attraction_object["av_begin"],
                        attraction_object["av_end"],
                        attraction_object["idpt"],
                        attraction_object["memo_time"],
                        attraction_object["poi"],
                        attraction_object["rate"],
                        attraction_object["ref_wp"])
                       )
        mysql_connection.commit()
        print("insert attraction info success!")
    except Exception as err:
        print("error in insert_attraction_info")
        print(err)

    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
        cursor.close()
        mysql_connection.close()

def insert_image(attraction_id, src):
    mysql_connection = get_mysql_connection_from_pool(mysql_connection_pool)
    cursor = mysql_connection.cursor(dictionary=True)
    mysql_str = "INSERT INTO image(attraction_id, src) VALUES (%s, %s)"
    try:
        cursor.execute(mysql_str, 
                       (attraction_id,
                        src)
                       )
        mysql_connection.commit()
        print("insert into image success!")
    except Exception as err:
        print(err)
    finally:
        if mysql_connection.in_transaction:
            mysql_connection.rollback()
        cursor.close()
        mysql_connection.close()    
