import mysql.connector
import attraction_model_config as config


db_fig ={
    'host':config.MYSQL_HOST,
    'user':config.MYSQL_USER,
    'password':config.MYSQL_PASSWORD,
    'database':config.MYSQL_DATABASE,
    "pool_name":"mysql_pool",
    "pool_size":10
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
        
