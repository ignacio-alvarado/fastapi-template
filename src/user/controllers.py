from fastapi import Depends
from pymongo import AsyncMongoClient
from config.db import get_db
from typing import Annotated

from user.models import User

async def list_users(db: Annotated[AsyncMongoClient, Depends(get_db)]) -> list[User]:
    """
    List all users.
    """
    user_collection = db.get_collection("users")
    users = await user_collection.find().to_list(length=None)
    return [User(**user) for user in users]

