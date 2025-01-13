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