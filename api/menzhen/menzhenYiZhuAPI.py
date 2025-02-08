from fastapi import APIRouter,Request
from pydantic import BaseModel
from db.database import execute_query,commit_query,get_mssql_connection
from db.sql.menzhen.menzhenyizhuSQL import *
import xml.etree.ElementTree as ET
import pymssql
import logging


logger = logging.getLogger(__name__)

menzhenYiZhuAPI = APIRouter(prefix="/menzhenyizhu",tags=["门诊医嘱"])


class SearchContent(BaseModel):
    content:str = ''
    keshiId:str = ''

@menzhenYiZhuAPI.post("/getICD10Code")
async def getICD10Code(request:Request,searchContent:SearchContent):
    '''
    获取ICD10编码
    '''
    responJson = {}
    if searchContent.content == '':
        responJson = {'code':1,'result':'请输入搜索内容'}
        return  responJson
    content = '%' + searchContent.content + '%'
    rows, columns = execute_query(getICD10CodeSQL,(content,content,content))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson



@menzhenYiZhuAPI.post("/getYiZhuContent")
async def getYiZhuContent(request:Request,searchContent:SearchContent):
    '''
    获取医嘱内容
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid

    responJson = {}
    
    if searchContent.keshiId == '':
        return {'code':1,'result':'请选择科室'}
    keshiId = searchContent.keshiId
    if searchContent.content == '':
        responJson = {'code':1,'result':'请输入搜索内容'}
        return  responJson
    content = '%' + searchContent.content + '%'
    rows, columns = execute_query(getYiZhuContentSQL,(content,keshiId,fryid))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson



@menzhenYiZhuAPI.get("/getGeiYaoTuJing")
async def getGeiYaoTuJing(request:Request):
    '''
    获取给药途径
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid
    rows, columns = execute_query(getGeiYaoTuJingSQL,(fryid,))
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    
@menzhenYiZhuAPI.get("/getPinci")
async def getPinci(request:Request):
    '''
    获取频次
    '''
    rows, columns = execute_query(getPinciSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    

@menzhenYiZhuAPI.get('/getYongYaoMuDi')
async def getYongYaoMuDi(request:Request):
    '''
    获取用药目的
    '''
    rows, columns = execute_query(getYongYaoMuDiSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    

@menzhenYiZhuAPI.get('/getYiZhuBeiZhu')
async def getYiZhuBeiZhu(request:Request):
    '''
    获取医嘱备注
    '''
    rows, columns = execute_query(getYiZhuBeiZhuSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    

@menzhenYiZhuAPI.get('/getZhiXingKeShi')
async def getZhiXingKeShi(request:Request):
    '''
    获取执行科室
    '''
    rows, columns = execute_query(getZhiXingKeShiSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    


@menzhenYiZhuAPI.get('/getGeiYaoZhiXingKeShi')
async def getGeiYaoZhiXingKeShi(request:Request):
    '''
    获取给药执行科室
    '''
    rows, columns = execute_query(getGeiYaoZhiXingKeShiSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }