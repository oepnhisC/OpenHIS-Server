from fastapi import APIRouter,Request
from pydantic import BaseModel
from db.database import execute_query,commit_query,get_mssql_connection
from db.sql.menzhen.menzhenSQL import *
import xml.etree.ElementTree as ET
import pymssql
import logging


logger = logging.getLogger(__name__)

menzhenAPI = APIRouter(prefix="/menzhen",tags=["门诊"])

class JiuZhenXinXi(BaseModel):
    jzid:str




@menzhenAPI.post('/getHouZhenList')
async def getHouZhenList(request:Request):
    '''
    获取候诊列表
    '''
    responJson = {}
    rows, columns = execute_query(getHouZhenListSQL,())
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson


@menzhenAPI.post('/getJiuZhenList')
async def getJiuZhenList(request:Request):
    '''
    获取就诊列表
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid
    responJson = {}
    rows, columns = execute_query(getJiuZhenListSQL,())
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson


@menzhenAPI.post('/getYiZhuList')
async def getYiZhuList(request:Request,jiuZhenXinXi:JiuZhenXinXi):
    '''
    获取医嘱列表
    '''
    if not jiuZhenXinXi.jzid:
        return {'code':2,'result':'无就诊ID'}
    responJson = {}
    rows, columns = execute_query(getYiZhuListSQL,(jiuZhenXinXi.jzid,))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson

class ChaXunBingRen(BaseModel):
    beginTime:str
    endTime:str
    content:str
    mzh:str


@menzhenAPI.post('/chaXunBingRen')
def chaXunBingRen(request:Request,chaxunBingRen:ChaXunBingRen):
    '''
    搜索病人信息
    '''
    responJson = {}
    if not chaxunBingRen.beginTime or not chaxunBingRen.endTime :
        return {'code':2,'result':'必须选择时间范围'}
    if not chaxunBingRen.content:
        return {'code':2,'result':'必须输入搜索内容'}
    rows, columns = execute_query(chaXunOneBingRenSQL
                        ,(chaxunBingRen.beginTime ,chaxunBingRen.endTime
                          ,chaxunBingRen.content ,chaxunBingRen.mzh
                          ,chaxunBingRen.content ,chaxunBingRen.content,chaxunBingRen.content))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson



@menzhenAPI.post('/getBingRenXinXi')
async def getBingRenXinXi(request:Request,jiuzhen:JiuZhenXinXi):
    '''
    获取病人详细信息
    '''
    responJson = {}
    if not jiuzhen.jzid:
        return {'code':2,'result':'无就诊ID'}
    rows, columns = execute_query(getBingRenXinXiSQL,(jiuzhen.jzid,jiuzhen.jzid))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson



@menzhenAPI.get('/getKeShi')
async def getKeShi(request:Request):
    '''
    获取科室信息
    '''
    responJson = {}
    
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid

    rows, columns = execute_query(getKeShiSQL,(fryid,))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson


class GuaHaoInfo(BaseModel):
    jzid:str = '0'  #就诊ID
    brid:str = '0'  #病人ID
    mzh:str = ''  #门诊号
    yykh:str = '' #会员卡号
    kh:str = '' #卡号
    yyid:str='0' #会员ID
    zjlx:str = '01' #证件类型
    sfz:str = '' #身份证号码
    qtzj:str = '' #其他证件
    name:str  #姓名
    pingyin:str = '' #拼音
    wubi:str = '' #五笔
    sex:str = '1' #性别
    xxnl:str  #详细年龄
    zy:str = '' #职业
    hunyin :str = '9' #婚姻状况
    guoji :str='' #国籍
    minzu :str = '' #民族
    brlb :str='自费' #病人类别
    fkfs :str = '' #付款方式
    telephone:str = '' #联系电话
    mobilephone:str = '' #手机号
    sheng : str = '' #省
    shi : str = '' #市
    zhuzhi:str = '' #住址
    jsr : str = '' #介绍人
    momo:str = '' #备注
    zhengzhuang:str = '' #症状体征
    gzdw:str = '' #工作单位
    dwdh:str = '' #单位电话
    dwdz:str = '' #单位地址
    ghksid:str #挂号科室ID
    cfz:str = '0' #初复诊
    birthday:str = '' #出生日期
    
@menzhenAPI.post('/jianYiGuaHao')
async def jianYiGuaHao(request:Request,guaHaoInfo:GuaHaoInfo):
    '''
    简易挂号
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid
    fryno = request.app.state.username
    fname = request.app.state.fname

    responJson = {}
    root = ET.Element("Root")

    NODE = ET.SubElement(root, "NODE")

    # 创建 Ie 元素并设置属性
    ie = ET.SubElement(NODE, "Ie", {
        "jzid": guaHaoInfo.jzid,
        "brid": guaHaoInfo.brid,
        "mzh": guaHaoInfo.mzh,
        "yykh": guaHaoInfo.yykh,
        "yyid": guaHaoInfo.yyid,
        "zjlx": guaHaoInfo.zjlx,
        "sfz": guaHaoInfo.sfz,
        "qtzj": guaHaoInfo.qtzj,
        "name": guaHaoInfo.name,
        "pingyin": guaHaoInfo.pingyin,
        "sex": guaHaoInfo.sex,
  
    })

    xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

    conn = get_mssql_connection()
    cursor = conn.cursor()
    responJson = {'code':1,'result':'失败'}
    try:
        logger.info('开始挂号')
        logger.info(xml_string)
        msg = cursor.callproc('GuaHao',  (xml_string,0,pymssql.output(int) ,pymssql.output(int),pymssql.output(str),pymssql.output(int),pymssql.output(str)) )   
        result = {
            "jzid":msg[2],
            'brid':msg[3],
            'mzh':msg[4],
            'djid':msg[5],
            'msg':msg[6]
        }
        logger.info('挂号结果：'+str(result))
        responJson = {'code':0,'result':result}
    except(Exception) as e:
        error_code = e.args[0]
        error_message_bytes = e.args[1]
        error_message = error_message_bytes.decode('utf-8')
        logger.info(f"错误代码：{error_code}")
        logger.info(f"错误信息：{error_message}")
        responJson = {'code':2,'result':'挂号失败，请联系管理员'}
    finally:
        cursor.close()
        conn.close()

    return responJson

class SearchContent(BaseModel):
    content : str 
    mzh :str 

@menzhenAPI.post('/getOldData')
async def getOldData(request:Request,searchContent:SearchContent):
    '''
    获取旧数据
    '''
    responJson = {}
    if not searchContent.content:
        return {'code':2,'result':'无搜索内容'}
    logger.info('开始查询')
    logger.info('查询内容:'+searchContent.content)
    rows, columns = execute_query(getOldDataSQL,(searchContent.content ,searchContent.mzh ,searchContent.content ,searchContent.content,searchContent.content))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson