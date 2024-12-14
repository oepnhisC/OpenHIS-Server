from fastapi import APIRouter,Request
from db.database import execute_query,commit_query
from pydantic import BaseModel
from fastapi.routing import APIRoute
from db.sql.manager.permissionManagerSQL import *


permissionManagerAPI = APIRouter(prefix="/permissionManger", tags=["权限管理"])


@permissionManagerAPI.post("/addPermission")
async def addPermission(request:Request):


    

    responJson = {'code':1,'result':'添加成功'}
    return responJson



@permissionManagerAPI.get("/getAllAPI")
async def getAllAPI(request:Request):
    '''
    获取所有API
    '''
    responJson = {}
    allapi = []
    for route in request.app.routes:
        if isinstance(route, APIRoute):
            print(route.path)
            allapi.append({'url':route.path})

    responJson = { 'code':0,'result':allapi }

    return responJson





@permissionManagerAPI.get("/getPermissionList")
async def getPermissionList(request:Request):
    '''
    获取权限列表
    '''
    responJson = {}

    rows, columns = execute_query(getPermissionListSQL,())
    if len(rows) == 0:
        responJson = { 'code':1,'result':'没有查到数据' }
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data  }

    return responJson


