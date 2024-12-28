from fastapi import APIRouter,Request
from db.database import execute_query,commit_query
from db.sql.menzhen.menzhenSQL import *

menzhenAPI = APIRouter(prefix="/menzhen",tags=["门诊"])


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
