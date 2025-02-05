from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from models.user_requests import User
from services.exceptions.auth_exception import CredentialsException
from services.repositories.generative_ai_repositories import GenerativeAiRepository
from services.utils.aws_parameter_store import get_parameter_store_value

app = FastAPI()
generative_ai_repository = GenerativeAiRepository()

# 보안 관련 설정
SECRET_KEY = get_parameter_store_value("/SECRET_KEY")
ALGORITHM = get_parameter_store_value("/ALGORITHM")

# 패스워드 해싱을 위한 CryptContext 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 스키마 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 패스워드 해싱 함수
def get_password_hash(password):
    return pwd_context.hash(password)


# 사용자 정보 가져오기
def get_user(userid: str):
    user_information = generative_ai_repository.select_user_information(userid)

    if user_information is None:
        print(f"User not found for userid: {userid}")
        return None
    
    try:
        return User(
            userid=user_information.userid,
            username=user_information.username,
            email=user_information.email,
            hashed_password=user_information.hashed_password
        )
    except AttributeError as e:
        print(f"Error Creating User object: {str(e)}")
        return None


# 패스워드 검증 함수
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 사용자 인증 함수
def authenticate_user(userid: str, password: str):
    user_information = get_user(userid)
    if not user_information:
        return False
    if not verify_password(password, user_information.hashed_password):
        return False
    return user_information


# JWT 토큰 생성 함수
def create_access_token(token_data: dict, expires_delta: timedelta):
    to_encode = token_data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 현재 사용자 정보 가져오기
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise CredentialsException("Token does not contain 'sub' field")
    except JWTError:
        raise CredentialsException("Invalid token")
    return username