from fastapi import APIRouter,Request
from db.database import get_connection,execute_query
from pydantic import BaseModel
from db.sql.user.userSQL import *
import jwt
from settings import jwtSECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from mysecurity import hash_password,verify_password
from datetime import datetime, timedelta


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
    if not verify_password(user.password, PasswordHash):
        responJson = {'code':2,'result':'用户或密码错误'}
        return responJson
    
    playload = {
        'username': user.username,
        'ip': request.client.host,
        'exp': datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    request.app.state.username = user.username
    print('ip:',request.client.host,'username:',user.username,'登录成功')
    print('exp:',playload['exp'])

    # 登录成功，生成token
    token = jwt.encode(playload,jwtSECRET_KEY, algorithm=ALGORITHM)
    responJson = { 'code':0,'result':token }
    return responJson
        
    