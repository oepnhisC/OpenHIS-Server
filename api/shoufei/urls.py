from fastapi import APIRouter
from db.database import * 
from db.sql.shoufei.paidList import paidListSQL

shoufeiAPI = APIRouter(prefix="/shoufei",tags=["收费"])

@shoufeiAPI.get("/")
async def index():
    return {"message": "收费"}





@shoufeiAPI.get("/paidList")
async def paidList():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(paidListSQL)
    rows = cursor.fetchall()
    # 获取列名
    columns = [column[0] for column in cursor.description]
    # 将每一行转换为字典
    data = [dict(zip(columns, row)) for row in rows]
 
    cursor.close()
    conn.close()
    return {"data": data}
