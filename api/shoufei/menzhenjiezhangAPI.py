from fastapi import APIRouter,Request
from db.database import * 
from pydantic import BaseModel


menzhenJZAPI  = APIRouter(prefix="/shoufei",tags=["门诊结账"])


class JieZhangID(BaseModel):
    id:int

@menzhenJZAPI.post("/tuifei")
async def tuifei(request:Request,jiezhangID:JieZhangID):
    return {"code":200,"msg":"成功"}
