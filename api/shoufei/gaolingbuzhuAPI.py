from fastapi import APIRouter,Request
from db.database import * 
from pydantic import BaseModel
from db.sql.baobiao.shoufei.gaolingjisuanSQL import gaolingjisuanSQL,GaoLingZiFeiHuiZongSQL


gaolingbuzhuAPI = APIRouter(prefix="/shoufei",tags=["高龄补助"])


@gaolingbuzhuAPI.get("/gaolingjifeibiao")
async def gaolingjifeibiao(request: Request):
    '''
    高龄补助自费表
    '''

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(gaolingjisuanSQL)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson



@gaolingbuzhuAPI.get("/gaolingjifeihuizong")
async def gaolingjifeihuizong(request: Request):
    '''
    高龄补助自费汇总表
    '''

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(GaoLingZiFeiHuiZongSQL)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson