from fastapi import APIRouter,Request
from db.database import execute_query
from db.sql.gonggong.gonggongSQL import *
import logging

gonggongAPI = APIRouter(prefix="/gonggong",tags=["公共模块"])

logger = logging.getLogger(__name__)

@gonggongAPI.get("/getAddress")
async def getAddress(request:Request):
    """
    获取地区信息
    """
    logger.info("获取地区信息")
    responJson = {}
    sheng = []
    shi = []
    qu = []
    zhen = []

    # 查询省份信息
    rows,columns = execute_query(shengSQL,())
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        sheng = [dict(zip(columns, row)) for row in rows]
        
    # 查询城市信息
    rows,columns = execute_query(shiSQL,())
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        shi = [dict(zip(columns, row)) for row in rows]

    # 查询区县信息
    rows,columns = execute_query(quSQL,())
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        qu = [dict(zip(columns, row)) for row in rows]

    # 查询镇信息
    rows,columns = execute_query(zhenSQL,())
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        zhen = [dict(zip(columns, row)) for row in rows]

    responJson = {'code':0,'result':{'sheng':sheng,'shi':shi,'qu':qu,'zhen':zhen}}
    

    return responJson