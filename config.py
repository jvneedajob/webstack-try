#encoding: utf-8
import os
from datetime import timedelta
DEBUG = True

SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

DIELECT= 'mysql'
DRIVE = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'project'
SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIELECT,DRIVE,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = True