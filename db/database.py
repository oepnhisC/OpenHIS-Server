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
                       , database=dbName,charset='utf8'
                       ,autocommit=True
                       )
    return conn

def get_mssql_connection():
    conn = pymssql.connect(server=dbIP, user=dbUser, password=dbPassword
                       , database=dbName
                       ,charset='utf8'
                       ,autocommit=True
                       )
    return conn

def get_mssql_connection_cp936():
    conn = pymssql.connect(server=dbIP, user=dbUser, password=dbPassword
                       , database=dbName
                       ,charset='cp936'
                       ,autocommit=True
                       )
    return conn

def execute_query(sql:str, parameter):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql,parameter)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    return rows,columns



def commit_query(sql:str, parameter):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql,parameter)
    conn.commit()
    cursor.close()
    conn.close()