from fastapi import APIRouter,Request
from yibao.info import * 
from db.database import get_connection
from db.sql.zizhuji.danju import jieZhangDanjuSQL


danjuAPI = APIRouter(prefix="/zizhuji",tags=["自助机"])


# 查询结账单据
@danjuAPI.get("/jiezhangdanju")
async def danju(request:Request):
    sfz =request.app.state.sfz
    qtzj =request.app.state.qtzj 
    if (sfz == '' and qtzj == ''):
        responJson = {'code':99,'result':'无身份证信息'}
        return  responJson

    zj = ''
    if sfz != '':
        zj = sfz
    elif qtzj != '':
        zj = qtzj

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(jieZhangDanjuSQL, (zj,zj))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson