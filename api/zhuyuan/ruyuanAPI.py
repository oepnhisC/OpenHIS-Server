from fastapi import APIRouter,Request
from pydantic import BaseModel,constr, validator
from mylogging import logger
from db.database import get_connection, execute_query
from db.sql.zhuyuan.ruyuanSQL import ruyuanSQL01 

from fastapi import FastAPI, APIRouter, Request, HTTPException
from datetime import datetime
import logging

# 设置日志记录
logger = logging.getLogger(__name__)

ruyuanAPI = APIRouter(prefix="/zhuyuan", tags=["病人入院管理"])

class Shijian(BaseModel):
    begintime: datetime  # 开始时间，使用datetime类型
    endtime: datetime    # 结束时间，使用datetime类型

@ruyuanAPI.post("/getdata")
async def ruyuan(request: Request, shijian: Shijian):
    """
    入院病人信息查询
    """
    
        # 从输入对象中获取时间范围
    begintime = shijian.begintime
    endtime = shijian.endtime
        
    print(f"转换后的查询日期范围: {begintime} 至 {endtime}")  # 为调试打印日期范围


    # 执行查询语句
    rows, columns =  execute_query(ruyuanSQL01, (begintime.isoformat(), endtime.isoformat()))

    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson


   
   
        
        
   
