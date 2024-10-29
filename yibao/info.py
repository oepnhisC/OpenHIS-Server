import time
import random
import hashlib
from datetime import datetime

# 固定字符集
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
numbers = "0123456789"

#填入自己医院的相关信息
paasid = 'paasid'
secretKey = 'secretKey'
hospitalID = 'hospitalID'
hospitalName = 'hospitalName'
mdtrtarea_admvs = '123456'

#接口地址
url = 'http://xxxxx/'


def create_request_Data(infno,inputJson,insuplc_admdvs=mdtrtarea_admvs):
    requestURL = url + infno
    timestamp = str(int(time.time()))
    nonce = ''.join(random.choice(characters) for _ in range(32))
    signature = hashlib.sha256( (timestamp+secretKey+nonce+timestamp).encode('utf-8') ).hexdigest()
    posthead = {
    'Content-Type':'application/json',
    'x-tif-paasid':paasid,
    'x-tif-signature':signature,
    'x-tif-timestamp':timestamp,
    'x-tif-nonce':nonce
    }

    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    snumber = ''.join(random.choice(numbers) for _ in range(4))
    msgid = hospitalID + current_time + snumber

    postdata = {
            "infno": infno,
            "msgid": msgid,
            "mdtrtarea_admvs": mdtrtarea_admvs,
            "insuplc_admdvs": insuplc_admdvs,
            "recer_sys_code": "13888",
            "dev_no": "",
            "dev_safe_info": "",
            "cainfo": "",
            "signtype": "",
            "infver": "V1.0",
            "opter_type": "2",
            "opter": "13888",
            "opter_name": "自助机",
            "inf_time" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "fixmedins_code": hospitalID,
            "fixmedins_name": hospitalName,
            "sign_no": "",
            "enc_type":"",
            "input": inputJson
        }
    return requestURL,postdata,posthead