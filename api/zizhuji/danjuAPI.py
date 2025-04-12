from fastapi import APIRouter,Request
from yibao.info import * 
from db.database import execute_query
from db.sql.zizhuji.danJuSQL import *


danjuAPI = APIRouter(prefix="/zizhujiDanJu",tags=["自助机单据"])


@danjuAPI.get("/getYiJieZhangDanJu")
async def getYiJieZhangDanJu(request:Request):
    '''
    查询已结账单据
    '''
    if not hasattr(request.app.state,'ryidList'):
        return {'code':2,'result':'无登录信息'}
    
    ryidList =request.app.state.ryidList 
    listStr = ','.join(map(str, ryidList))
    rows,columns = execute_query(getYiJieZhangDanjuSQL, listStr)
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
   
    return  responJson



@danjuAPI.get("/getDaiJieZhangDanJu")
def getDaiJieZhangDanJu(request: Request):
    '''
    获取待结账单据
    '''
    if not hasattr(request.app.state,'ryidList'):
        return {'code':2,'result':'无登录信息'}

    ryidList =request.app.state.ryidList 
    listStr = ','.join(map(str, ryidList))
    rows,columns = execute_query(getDaiJieZhangDanJuSQL, listStr)
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson