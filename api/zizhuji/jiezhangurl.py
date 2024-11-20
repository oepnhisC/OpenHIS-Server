from fastapi import APIRouter,Request
from yibao.info import * 
from pydantic import BaseModel
import requests
import json
from db.database import get_connection,get_JieZhang_connection
import xml.etree.ElementTree as ET
import pymssql


zizhuji_jiezhangAPI = APIRouter(prefix="/zizhuji",tags=["自助机结账"])



# 本地结账
@zizhuji_jiezhangAPI.get('/jiezhang')
def jiezhang(request: Request):
    fjzid = request.app.state.info['fjzid']
    djhlist = request.app.state.info['fdjh']
   

    root = ET.Element()
    # 获取金额数据
    # ...

    # 获取单据数据
    # ...

    xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
    print('xml_string',len(xml_string))
    conn = get_JieZhang_connection()
    cursor = conn.cursor()
    responJson = {'code':1,'result':'失败'}
    try:
        # 执行存储过程
        msg = cursor.callproc('JieZhang_ZZJ',  (xml_string,fjzid,pymssql.output(int),pymssql.output(str)) )   
        print(msg[1],msg[2])
        responJson = {'code':0,'result':msg[2]}
        # 记录结账id
        request.app.state.jzid = msg[2]
    except(Exception) as e:
        # 获取状态码和错误信息
        error_code = e.args[0]
        error_message_bytes = e.args[1]
        # 将字节字符串解码为普通字符串
        error_message = error_message_bytes.decode('utf-8')
        print(f"错误代码：{error_code}")
        print(f"错误信息：{error_message}")
        responJson = {'code':2,'result':'结账失败，请联系管理员'}
    finally:
        cursor.close()
        conn.close()

    return  responJson
