from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from models.user_requests import User
from services.auth import authenticate_service
from services.exceptions.auth_exception import CredentialsException

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 로그인 과정 중 ACCESS TOKEN 발급하는 함수
@router.post('/token')
async def login(credentials: OAuth2PasswordRequestForm = Depends()):
    user_information = authenticate_service.authenticate_user(credentials.username, credentials.password)

    if not user_information:
        raise CredentialsException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authenticate_service.create_access_token(
        token_data={"sub": user_information.userid, "username": user_information.username}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Frontend <PRIVATEROUTE> 접근할 때마다 TOKEN 인증을 위한 함수
@router.get("/verify")
async def token_verify(current_user: User = Depends(authenticate_service.get_current_user)):
    return current_user


# SAMPLE PASSWORD 발급을 위한 함수
@router.get("/get_hashed_password")
async def return_hashed_password(password: str):
    return authenticate_service.get_password_hash(password)
