from fastapi import APIRouter,Request
from pydantic import BaseModel
from db.database import execute_query,commit_query
from db.sql.menzhen.menzhenSQL import *

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
                        ,(chaxunBingRen.beginTime
                          ,chaxunBingRen.endTime
                          ,chaxunBingRen.content
                          ,chaxunBingRen.content
                          ,chaxunBingRen.mzh
                          ,chaxunBingRen.content))
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

