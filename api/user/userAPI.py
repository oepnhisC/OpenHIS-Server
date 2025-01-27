from fastapi import APIRouter,Request
from db.database import commit_query,execute_query
from pydantic import BaseModel
from db.sql.user.userSQL import *
import jwt
from settings import jwtSECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from mysecurity import hash_password,verify_password
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

userAPI = APIRouter(prefix="/user", tags=["用户"])


class User(BaseModel):
    username: str
    password: str

@userAPI.post("/login")
async def login(request: Request, user: User):
    responJson = {}
    if not user.username or not user.password:
        responJson = {'code':2,'result':'用户名或密码不能为空'}
        return responJson
    
    rows,columns = execute_query(getUserSQL,(user.username,))
    if len(rows) == 0:
        responJson = {'code':2,'result':'用户或密码错误'}
        return  responJson
    


    data = [dict(zip(columns, row)) for row in rows]
    PasswordHash = data[0]['PasswordHash']
    fname = data[0]['fname']
    fryid = str(data[0]['fryid'])
    fksid = str(data[0]['fksid'])
    fks = data[0]['fks']
    if not verify_password(user.password, PasswordHash):
        responJson = {'code':2,'result':'用户或密码错误'}
        return responJson
    
    playload = {
        'username': user.username,
        'ip': request.client.host,
        'exp': datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    request.app.state.username = user.username
    request.app.state.fryid = fryid
    request.app.state.fksid = fksid
    request.app.state.fname = fname
    print('ip:',request.client.host,'username:',user.username,'登录成功')
    print('exp:',playload['exp'])

    # 登录成功，生成token
    token = jwt.encode(playload,jwtSECRET_KEY, algorithm=ALGORITHM)

    rows,columns = execute_query(getUserPermissionSQL,(user.username,))
    request.app.state.permissions = rows
    permissions = [dict(zip(columns, row)) for row in rows]

    logger.info('登录成功,姓名:'+fname+',ID:'+fryid+',IP:'+request.client.host)
    responJson = { 'code':0,'result':token ,'permission':permissions ,'fname':fname ,'ip':request.client.host,'fks':fks,'fksid':fksid }
    return responJson
        

@userAPI.post('/logout')
async def logout(request: Request):
    '''
    退出登录
    '''
    request.app.state.username = None
    return {'code':0,'result':'退出登录成功'}


class ChangePassword(BaseModel):
    oldPassword: str
    newPassword: str


@userAPI.post('/changePassword')
async def changePassword(request: Request, password: ChangePassword):
    '''
    修改密码
    '''
    if not password.oldPassword or not password.newPassword:
        return {'code':2,'result':'用户名或密码不能为空'}
    
    if request.app.state.username is None:
        return {'code':2,'result':'请先登录'}
    
    username = request.app.state.username
    rows,columns = execute_query(getUserSQL,(username,))
    
    data = [dict(zip(columns, row)) for row in rows]
    PasswordHash = data[0]['PasswordHash']
    if not verify_password(password.oldPassword , PasswordHash):
        return {'code':2,'result':'原密码错误'}
    
    newPasswordHash = hash_password(password.newPassword)
    try:
        commit_query(updatePasswordSQL,(newPasswordHash,username))
    except Exception as e:
        print(e)
        return {'code':2,'result':'修改密码失败'}
    return {'code':0,'result':'密码修改成功'}

