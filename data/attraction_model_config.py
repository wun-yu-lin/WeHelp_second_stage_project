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
