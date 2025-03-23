from fastapi import APIRouter,Request
from pydantic import BaseModel,constr, validator
from db.database import get_connection, execute_query
from db.sql.zhuyuan.ruyuanSQL import ruyuanSQL01 
from db.sql.zhuyuan.bingzhongSQL import bingzhongSQL01
from typing import List, Dict, Any
from db.sql.zhuyuan.bingmaSQL import bingmaSQL01
from db.sql.zhuyuan.gongshangmaSQL import gongshangmaSQL01


from fastapi import FastAPI, APIRouter, Request, HTTPException
from datetime import datetime
import logging
import re

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


@ruyuanAPI.post("/getbingzhong")

async def getbingzhong(request: Request) -> Dict[str, Any]:
    """
    获取病种统计数据
    """
    try:
        # 可能需要从请求中提取参数，例如筛选条件或其他信息
        params = request.query_params.get("some_param", None)  # 假设您从请求中获取参数
        
        # 执行查询语句，假设 execute_query 需要 SQL 查询和查询参数
        rows, columns = execute_query(bingzhongSQL01, ())  # 传递参数给查询

        # 将查询结果封装为字典
        data = [dict(zip(columns, row)) for row in rows]
        str = {"code": 0, "result": data}
        
        return str

    except Exception as e:
        logger.error(f"获取病种统计数据失败: {e}")
        return {"code": "error", "message": "获取病种统计数据失败"}  # 假设您需要返回错误信息  


@ruyuanAPI.post("/bingma")
async def bingma(request: Request) -> Dict[str, Any]:
    """
    获取普通医保病马统计数据
    """
    try:
        # 从请求中提取筛选参数，例如分页参数和其他信息
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))  # 默认每页10条
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 执行查询语句，通过传递参数
        rows, columns = execute_query(bingmaSQL01, (offset, page_size))  # 传递 offset 和 page_size
        
        # 将查询结果封装为字典
        data = [dict(zip(columns, row)) for row in rows]

        return {"code": 0, "result": data}

    except Exception as e:
        logger.error(f"获取病马统计数据失败: {e}")
        return {"code": "error", "message": "获取病马统计数据失败"}  # 返回错误信息 
    

@ruyuanAPI.post("/gongshangma")
async def gongshangma(request: Request) -> Dict[str, Any]:
    """
    获取工伤病马统计数据
    """
    try:
        # 可能需要从请求中提取参数，例如筛选条件或其他信息
        params = request.query_params.get("some_param", None)  # 假设您从请求中获取参数
        
        # 执行查询语句，假设 execute_query 需要 SQL 查询和查询参数
        rows, columns = execute_query(gongshangmaSQL01, ())  # 传递参数给查询

        # 将查询结果封装为字典
        data = [dict(zip(columns, row)) for row in rows]
        str = {"code": 0, "result": data}
        
        return str

    except Exception as e:
        logger.error(f"获取供应商病马统计数据失败: {e}")
        return {"code": "error", "message": "获取供应商病马统计数据失败"}  # 假设您需要返回错误信息  