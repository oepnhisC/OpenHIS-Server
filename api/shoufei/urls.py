from fastapi import APIRouter,Request
from db.database import * 
from pydantic import BaseModel
from db.sql.shoufei.jiezhangdanjuSQL import jiezhangdanjuSQL

shoufeiAPI = APIRouter(prefix="/shoufei",tags=["收费"])


class ShiJian(BaseModel):
    begintime: str
    endtime: str

@shoufeiAPI.post("/jiezhangdanju")
async def jiezhangdanju(request: Request,shijian: ShiJian):

    print(shijian.dict())
    if not shijian.begintime or not shijian.endtime:
        responJson = {'code':1,'result':'时间不能为空'}
        return  responJson

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(jiezhangdanjuSQL,(shijian.begintime,shijian.endtime
                                     ,shijian.begintime,shijian.endtime
                                     ,shijian.begintime,shijian.endtime
                                     ,shijian.begintime,shijian.endtime))
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
