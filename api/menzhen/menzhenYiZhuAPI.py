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
    content:str

@menzhenYiZhuAPI.post("/getICD10Code")
async def getICD10Code(request:Request,searchContent:SearchContent):
    '''
    获取ICD10编码
    '''
    responJson = {}
    rows, columns = execute_query(getICD10CodeSQL,(searchContent.content,searchContent.content,searchContent.content))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson
