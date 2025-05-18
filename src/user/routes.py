from fastapi import APIRouter, Depends
from pymongo import AsyncMongoClient
from config.db import get_db
from typing import Annotated

from auth.utils.authorization import UserPermissionChecker
from user.models import User
from user.controllers import list_users

user_router = APIRouter()

@user_router.get("")
async def get_users(db: Annotated[AsyncMongoClient, Depends(get_db)], _: Annotated[User, Depends(UserPermissionChecker(roles=["admin"]))]) -> list[User]:
    users = await list_users(db)
    return users

@user_router.get("/me")
async def get_me(user: Annotated[User, Depends(UserPermissionChecker(roles=["admin", "user"]))]) -> User:
    return user