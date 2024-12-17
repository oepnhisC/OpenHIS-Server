from fastapi import APIRouter,Request
from db.database import execute_query,commit_query
from pydantic import BaseModel
from fastapi.routing import APIRoute
from db.sql.manager.permissionManagerSQL import *


permissionManagerAPI = APIRouter(prefix="/permissionManger", tags=["权限管理"])

class Permission(BaseModel):
    url:str
    name:str


class Role(BaseModel):
    name:str


class RolePermission(BaseModel):
    RoleID:str
    PermissionID:str


class RoleId(BaseModel):
    id:str

@permissionManagerAPI.post("/addPermission")
async def addPermission(request:Request,permission:Permission):
    '''
    添加权限
    '''
    if not permission.name or not permission.url:
        responJson = {'code':1,'result':'参数不能为空'}
        return responJson
    
    rows, columns = execute_query(selectOnePermissionSQL,(permission.url))
    if len(rows) > 0:
        responJson = {'code':1,'result':'权限已存在'}
        return responJson

    try:
        commit_query(addPermissionSQL,(permission.name,permission.url))
    except Exception as e:
        print(e)
        responJson = {'code':2,'result':'操作失败'}
        return responJson
    
    responJson = {'code':0,'result':'添加成功'}
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



@permissionManagerAPI.get('/getRoleList')
async def getRoleList(request:Request):
    '''
    获取角色列表
    '''
    responJson = {}

    rows, columns = execute_query(getRoleListSQL,())
    if len(rows) == 0:
        responJson = { 'code':1,'result':'没有查到数据' }
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data  }

    return responJson


@permissionManagerAPI.post('/addRole')
async def addRole(request:Request,role:Role):
    '''
    添加角色
    '''
    if not role.name:
        responJson = {'code':1,'result':'参数不能为空'}
        return responJson
    
    rows, columns = execute_query(selectOneRoleSQL,(role.name))
    if len(rows) > 0:
        responJson = {'code':1,'result':'角色已存在'}
        return responJson

    try:
        commit_query(addRoleSQL,(role.name))
    except Exception as e:
        print(e)
        responJson = {'code':2,'result':'操作失败'}
        return responJson
    
    responJson = {'code':0,'result':'添加成功'}
    return responJson


@permissionManagerAPI.post('/addPermissionToRole')
async def addPermissionToRole(request:Request,rolePermission:RolePermission):
    '''
    添加权限到角色
    '''
    if not rolePermission.RoleID or not rolePermission.PermissionID:
        responJson = {'code':1,'result':'参数不能为空'}
        return responJson
    
    rows, columns = execute_query(selectOnePermissionByIdSQL,(rolePermission.PermissionID))
    if len(rows) == 0:
        responJson = {'code':1,'result':'权限不存在'}
        return responJson

    rows, columns = execute_query(selectOneRoleByIdSQL,(rolePermission.RoleID))
    if len(rows) == 0:
        responJson = {'code':1,'result':'角色不存在'}
        return responJson


    rows, columns = execute_query(selectOnePermissionFromRoleSQL,(rolePermission.RoleID,rolePermission.PermissionID))
    if len(rows) > 0:
        responJson = {'code':1,'result':'角色已有此权限'}
        return responJson

    try:
        commit_query(addPermissionToRoleSQL,(rolePermission.RoleID,rolePermission.PermissionID))
    except Exception as e:
        print(e)
        responJson = {'code':2,'result':'操作失败'}
        return responJson
    
    responJson = {'code':0,'result':'添加成功'}
    return responJson



@permissionManagerAPI.post('/getRolesPermission')
async def getRolesPermission(request:Request,roleID:RoleId):
    '''
    获取角色权限
    '''
    if not roleID.id:
        responJson = {'code':1,'result':'参数不能为空'}
        return responJson
    
    rows, columns = execute_query(selectRolesPermissionSQL,(roleID.id))
    if len(rows) == 0:
        responJson = {'code':1,'result':'没有查到数据'}
        return responJson

    data = [dict(zip(columns, row)) for row in rows]
    responJson = {'code':0,'result':data}
    return responJson

