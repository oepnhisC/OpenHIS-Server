from fastapi import APIRouter
from yibao.info import * 
from pydantic import BaseModel
import requests
import json
from db.database import get_connection
from db.sql.zizhuji.payDetails import payDetailsSql
from db.sql.zizhuji.danju import danjuSQL,danjumingxiSQL,danjuZongJiaSQL




zizhujiAPI = APIRouter(prefix="/zizhuji",tags=["自助机"])


class PingZheng(BaseModel):
    number:str

# 电子医保凭证查询
@zizhujiAPI.post("/dzybpz")
def dzybpz(pingzheng:PingZheng):
    requestjson = {
        "data": {
            "mdtrt_cert_type": "01",
            "mdtrt_cert_no": pingzheng.number,
            "card_sn": "",
            "begntime": "",
            "psn_cert_type": "",
            "certno": "",
            "psn_name": ""
        }
    }
    
    requestURL,postdata,posthead = create_request_Data('1101',requestjson)
    response = requests.post(requestURL,data=postdata,headers=posthead)
    outputdata = json.loads(response.text)

    responJson = {'code':1,'result':'失败'}

    if outputdata :
        if outputdata['infcode'] == 0:
            print(outputdata['output'])
            
            certno =outputdata['output']['baseinfo']['certno']
            print(certno)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(payDetailsSql, (certno,))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            cursor.close()
            conn.close()
            print(rows)
            if len(rows) == 0:
                responJson = {'code':1,'result':'未查询到相关信息'}
            else:
                data = [dict(zip(columns, row)) for row in rows]
                responJson = { 'code':0,'result':data }
        
        else :
            print(outputdata['err_msg'])
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}

    return  responJson



@zizhujiAPI.post("/test")
def test(pingzheng:PingZheng):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(danjuSQL, ('AAABBB123','AAABBB123'))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    print(rows)
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return  responJson


class DanJuMingXi(BaseModel):
    fjzid:str
    fzyzd:str

# 单据明细
@zizhujiAPI.post('/danjumingxi')
def danjumingxi(danjumingxi:DanJuMingXi):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(danjumingxiSQL, (danjumingxi.fjzid,danjumingxi.fzyzd))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    print(rows)
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return  responJson

# 微信支付二维码
@zizhujiAPI.post('/wechatpayQRCode')
def wechatpayQRCode(danjumingxi:DanJuMingXi):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(danjuZongJiaSQL, (danjumingxi.fjzid,danjumingxi.fzyzd))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    print(row)
    if row[0] == '0':
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = {'money':row[0],'payurl':'http://www.baidu.com'}
        responJson = { 'code':0,'result':data }

    return  responJson



