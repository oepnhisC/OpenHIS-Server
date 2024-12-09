from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from mysecurity import hash_password,verify_password
import jwt
from settings import jwtSECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime

# 排除列表
excluded_paths = ["/user/login",'/userManger/addUser','/docs','/openapi.json']

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        
        resp = JSONResponse(content= {'code':999,'result':'未登录或登录过期，请重新登录'})

        # 检查请求路径是否在排除列表中
        if request.url.path in excluded_paths:
            response = await call_next(request)
            return response
        
        # 这里可以添加你的认证逻辑，例如检查 token
        token = request.headers.get("Authorization")
        if not token:
            return resp
        
        try:
            # 通常，Authorization头格式为 "Bearer <token>"
            token = token.split(" ")[1]  # 提取 token 部分
            payload = jwt.decode(token, jwtSECRET_KEY, algorithms=[ALGORITHM])  # 验证 token
            exp = payload['exp']  # 获取 token 过期时间
            now = datetime.now()  # 获取当前时间
            print(exp,now)
            if now > datetime.fromtimestamp(exp):  # 判断 token 是否过期
                return resp
            # else:
            #     #判断剩余时间,小于8分钟更新token
            #     remaining_time = exp - int(datetime.now().timestamp())
            #     if remaining_time < 480:
            #         new_token = jwt.encode({'username':payload['username'],'ip':request.client.host},jwtSECRET_KEY,algorithm=ALGORITHM)
            #         response = JSONResponse(content={'code':0,'result':new_token})
            if(request.app.state.username == payload['username'] and 
            request.client.host == payload['ip']):
                return await call_next(request)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return resp

        return resp

