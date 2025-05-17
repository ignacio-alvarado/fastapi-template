from auth.schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, RefreshRequest
from auth.controllers import register_user, get_token, refresh_token

from fastapi import APIRouter, Depends, HTTPException
from pymongo import AsyncMongoClient
from config.db import get_db
from typing import Annotated
from utils.logger import logger

auth_router = APIRouter()

@auth_router.post("/register")
async def register(request: RegisterRequest, db: Annotated[AsyncMongoClient, Depends(get_db)]) -> RegisterResponse:
    try:
        user_id = await register_user(request, db)
        return RegisterResponse(message=f"User registered with id: {user_id}")
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/login")
async def login(request: LoginRequest, db: Annotated[AsyncMongoClient, Depends(get_db)]) -> LoginResponse:
    try:
        tokens = await get_token(request, db)
        return LoginResponse(access_token=tokens['access_token'], refresh_token=tokens['refresh_token'])
    except Exception as e:
        logger.error(f"Error logging in: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    
@auth_router.post("/refresh")
async def refresh(request: RefreshRequest, db: Annotated[AsyncMongoClient, Depends(get_db)]) -> LoginResponse:
    try:
        tokens = refresh_token(request.refresh_token)
        return LoginResponse(access_token=tokens['access_token'], refresh_token=tokens['refresh_token'])
    except Exception as e:
        logger.error(f"Error refreshing token: {e}")
        raise HTTPException(status_code=401, detail=str(e))