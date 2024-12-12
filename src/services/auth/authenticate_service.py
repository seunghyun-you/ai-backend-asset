from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from models.user_requests import User
from services.exceptions.auth_exception import CredentialsException

app = FastAPI()

# 보안 관련 설정
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 패스워드 해싱을 위한 CryptContext 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 스키마 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 가상의 사용자 데이터베이스 (실제로는 데이터베이스에 저장해야 함)
poc_users_db = {
    "test": {
        "username": "SAMSUNGSDS",
        "email": "test@samsung.com",
        "hashed_password": '$2b$12$b35055Shd7Z0kkglS0JD8u/SjOWQQO/B1f3GsJXln0ojOK/sTxEBC'
    },
    "ajpoc": {
        "username": "AJ Network",
        "email": "AJ@samsung.com",
        "hashed_password": '$2b$12$hpFc9/f36Oh/FxlxYgkSTOLvHxGcL0RKYXwM6kb/ZuxoUub5G1Awq'
    }
}


# 패스워드 해싱 함수
def get_password_hash(password):
    return pwd_context.hash(password)


# 사용자 정보 가져오기
def get_user(username: str):
    if username in poc_users_db:
        user_dict = poc_users_db[username]
        return User(**user_dict)


# 패스워드 검증 함수
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 사용자 인증 함수
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 현재 사용자 정보 가져오기
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException("Token does not contain 'sub' field")
    except JWTError:
        raise CredentialsException("Invalid token")
    return username
