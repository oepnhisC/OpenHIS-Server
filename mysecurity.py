

from passlib.context import CryptContext

# 创建 CryptContext 实例
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    '''
    加密密码
    password: 明文密码
    return: 加密后的密码
    '''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    验证密码是否正确
    plain_password: 明文密码
    hashed_password: 加密后的密码
    return: 密码是否正确
    '''
    return pwd_context.verify(plain_password, hashed_password)
