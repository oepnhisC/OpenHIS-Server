import pyodbc
import pymssql
from settings import dbIP,dbName,dbUser,dbPassword

def get_connection():

    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER='+dbIP+';'
        'DATABASE='+dbName+';'
        'UID='+dbUser+';'
        'PWD='+dbPassword+';'
        )
    return conn


def get_JieZhang_connection():
    conn = pymssql.connect(server=dbIP, user=dbUser, password=dbPassword
                       , database=dbName,charset='cp936'
                       ,autocommit=True)
    return conn