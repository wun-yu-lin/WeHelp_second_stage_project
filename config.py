import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode. 
DEBUG = True

#database config
MYSQL_HOST = "localhost"
MYSQL_PASSWORD = "password"
MYSQL_USER = "root"
MYSQL_DATABASE = "taipei_travel"
MYSQL_POOL_SIZE=10



#sql filter string
SQL_FILTER_STRING = "-","and","exec","insert","select","delete","update","count","*","chr","mid","master","truncate","char","declare",";","or","-","+","="

##
# SET SESSION group_concat_max_len = 1000000;
GROUP_CONCAT_MAX_LEN = 1000000