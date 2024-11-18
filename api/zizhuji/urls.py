from fastapi import APIRouter,Request
from yibao.info import * 
from pydantic import BaseModel
import requests
import json
from db.database import get_connection
from db.sql.zizhuji.payDetails import payDetailsSql
from db.sql.zizhuji.danju import danjuSQL,danjumingxiSQL,danjuZongJiaSQL
from db.sql.zizhuji.print import printInfoHeaderSQL,zongFeiYongSQL,zhifuFangshiSQL,fapiaoURLSQL,feibieSQL,zhiyindanSQL,yingxiangdanSQL,zhuyaozhenduanSQL,weicaidanSQL,caixiedanSQL,fukedanSQL,jianyandanSQL,fapiaoSQL
from io import BytesIO
import fitz  # PyMuPDF
import base64


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
def test(request: Request, pingzheng:PingZheng):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(danjuSQL, ('AAABBB123','AAABBB123'))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    # print(rows)
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
        request.app.state.info = {'sfz':'AAABBB123'}
    
    return  responJson


class DanJuMingXi(BaseModel):
    fjzid:str
    fdjh:str

# 单据明细
@zizhujiAPI.post('/danjumingxi')
def danjumingxi(request: Request,danjumingxi:DanJuMingXi):
    djhlist = danjumingxi.fdjh.split(',')
    placeholders = ','.join('?' for _ in djhlist)
    newsql = danjumingxiSQL +f'({placeholders})'
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute( newsql, (danjumingxi.fjzid,)+tuple(djhlist) )
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
        request.app.state.info = {'sfz':request.app.state.info['sfz'],
                                   'fjzid':danjumingxi.fjzid,
                                    'fdjh':djhlist}
        request.app.state.ip = request.client.host
        
    return  responJson


# 微信支付二维码
@zizhujiAPI.get('/wechatpayQRCode')
def wechatpayQRCode(request: Request):
    fjzid = request.app.state.info['fjzid']
    djhlist = request.app.state.info['fdjh']
    placeholders = ','.join('?' for _ in djhlist)
    newsql = danjuZongJiaSQL +f'({placeholders})'
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(newsql, (fjzid,)+tuple(djhlist))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    print(row)
    if row[0] == '0':
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        request.app.state.amount = row[0]
        # 调用微信支付接口生成付款链接
        data = {'money':row[0],'payurl':'http://www.baidu.com'}
        responJson = { 'code':0,'result':data }
        

    return  responJson


# 打印信息
@zizhujiAPI.get('/printInfoHeader')
def printInfoHeader(request: Request):
    # djhlist = request.app.state.info['fjzid']
    fjzid = '587728'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(printInfoHeaderSQL, (fjzid))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return  responJson





# 费用信息
@zizhujiAPI.get('/feiYong')
def printInfoHeader(request: Request):
    # djhlist = request.app.state.info['fjzid']
    fjzid = '587728'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(zongFeiYongSQL, (fjzid))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    fzfy = 0
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        row=rows[0]
        fzfy = row[0]


    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(fapiaoURLSQL, (fjzid))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    furl = ''
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        row=rows[0]
        furl = row[0]
    

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(zhifuFangshiSQL, (fjzid))
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    fzffs = []
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        fzffs = [dict(zip(columns, row)) for row in rows]

    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(feibieSQL, (fjzid))
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    ffbs = []
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        ffbs = [dict(zip(columns, row)) for row in rows]

    


    responJson = { 'code':0,'fzfy':fzfy,'fzffs':fzffs ,'furl':furl ,'ffbs':ffbs }

    return  responJson

# 指引单
@zizhujiAPI.get('/zhiyindan')
def zhiyindan(request: Request):
    fjzid = '587723'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(zhiyindanSQL, (fjzid,fjzid))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    fzfy = 0
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson


# 主要诊断
@zizhujiAPI.get('/zhuyaozhenduan')
def zhuyaozhenduan(request: Request):
    fjzid = '587723'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(zhuyaozhenduanSQL, (fjzid))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    fzyzd = 0
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        row = rows[0]
        fzyzd = row[0]
        responJson = { 'code':0,'result':fzyzd }

    return  responJson

# 影像单
@zizhujiAPI.get('/yingxiangdan')
def yingxiangdan(request: Request):
    fjzid = '587723'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(yingxiangdanSQL, (fjzid,fjzid))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson


# 卫材领取单
@zizhujiAPI.get('/weicaidan')
def weicaidan(request: Request):
    fjzid = '585818'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(weicaidanSQL, (fjzid))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson




# 采血单
@zizhujiAPI.get('/caixiedan')
def caixiedan(request: Request):
    fjzid = '587743'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(caixiedanSQL, (fjzid))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson



# 妇科治疗单
@zizhujiAPI.get('/fukedan')
def fukedan(request: Request):
    fjzid = '587717'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(fukedanSQL, (fjzid))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson

# 检验条码
@zizhujiAPI.get('/jianyantiaoma')
def jianyantiaoma(request: Request):
    fjzid = '587743'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(jianyandanSQL, (fjzid))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson


# 发票信息
@zizhujiAPI.get('/fapiao')
def fapiao(request: Request):
    fjzid = '587728'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(fapiaoSQL, (fjzid))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(rows) == 0:

        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        row = rows[0]
        ffpurl = 'https://' +row[0]
        response = requests.get(ffpurl)
        result = []
        if response.status_code == 200:
            pdf_content = BytesIO(response.content)
    
            # 用PyMuPDF将PDF转换为图片
            doc = fitz.open("pdf", pdf_content)
            print(len(doc))
            # 遍历PDF中的每一页
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)  # 加载页面
                zoom_x = 2.0  # horizontal zoom
                zoom_y = 2.0  # vertical zoom
                mat = fitz.Matrix(zoom_x, zoom_y)
                pix = page.get_pixmap(matrix=mat) # 将页面转换为pixmap对象
                
                image_stream = BytesIO(pix.tobytes())
                image_stream.seek(0)
                image_data = image_stream.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                img_data = f'data:image/jpeg;base64,{image_base64}'
                result.append(img_data)


            # 关闭文档
            doc.close()
        else:
            responJson = {'code':1,'result':'未查询到相关信息'}
            return  responJson
        responJson = { 'code':0,'result':result }
    
    return  responJson
