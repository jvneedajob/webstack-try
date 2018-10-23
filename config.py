#encoding: utf-8
import os
DEBUG = True

SECRET_KEY = os.urandom(24)

DIELECT= 'mysql'
DRIVE = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'project'
SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIELECT,DRIVE,USERNAME,PASSWORD,HOST,PORT,DATABASE)