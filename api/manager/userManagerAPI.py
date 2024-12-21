from fastapi import APIRouter,Request
from db.database import execute_query,commit_query
from pydantic import BaseModel
from mysecurity import hash_password,verify_password
from db.sql.manager.userManagerSQL import *


userManagerAPI = APIRouter(prefix="/userManger", tags=["用户管理"])

class User(BaseModel):
    username:str
    password:str

@userManagerAPI.post("/addUser")
async def addUser(request:Request,user:User):

    if not user.username or not user.password:
        responJson = {'code':2,'result':'用户名或密码不能为空'}

    rows, columns = execute_query(selectUserSQL,(user.username,))
    if len(rows)!= 0:
        responJson = {'code':2,'result':'用户名已存在'}
        return responJson

    hashedPassword = hash_password(user.password)
    try:
        commit_query(addUserSQL,(user.username,hashedPassword))
    except Exception as e:
        print(e)
        responJson = {'code':2,'result':'用户添加失败'}
        return responJson

    responJson = {'code':0,'result':'用户添加成功'}
    return responJson



@userManagerAPI.get("/getUserList")
async def getUserList(request:Request):
    responJson = {}
    rows, columns = execute_query(getUserListSQL,())
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson


class UserID(BaseModel):
    id:int



@userManagerAPI.post("/getUserRoleList")
async def getUserRoleList(request:Request,userid:UserID):
    '''
    获取用户角色列表
    '''
    
    responJson = {}
    if not userid.id:
        responJson = {'code':2,'result':'用户ID不能为空'}
        return responJson
    
    rows, columns = execute_query(getUserRoleListSQL,(userid.id,))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson


class UserRole(BaseModel):
    userid:int
    roleid:int

@userManagerAPI.post("/addRoleToUser")
async def addRoleToUser(request:Request,userrole:UserRole):
    '''
    添加角色到用户
    '''
    responJson = {}
    if not userrole.userid or not userrole.roleid:
        responJson = {'code':2,'result':'用户ID或角色ID不能为空'}
        return responJson
    
    rows, columns = execute_query(selectOneUserRoleSQL,(userrole.userid,userrole.roleid))
    if len(rows)!= 0:
        responJson = {'code':2,'result':'该用户已有该角色'}
        return responJson

    try:
        commit_query(addRoleToUserSQL,(userrole.userid,userrole.roleid))
    except Exception as e:
        print(e)
        responJson = {'code':2,'result':'角色添加失败'}
        return responJson

    responJson = {'code':0,'result':'角色添加成功'}
    return responJson

