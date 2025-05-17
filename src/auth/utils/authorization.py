from fastapi import HTTPException, Depends
from pymongo import AsyncMongoClient
from fastapi.security import HTTPBearer
from typing import Annotated
from bson.objectid import ObjectId

from user.models import Role, User
from config.db import get_db
from auth.utils.token import verify_token

class UserPermissionChecker:
    """
    Check if a user has a permission to access a resource.
    """

    def __init__(self, roles: list[Role]):
        self.roles = roles

    async def __call__(self, token: Annotated[str, Depends(HTTPBearer())], db: Annotated[AsyncMongoClient, Depends(get_db)]) -> User:
        payload = verify_token(token.credentials)
        
        # Get user from db
        user_collection = db.get_collection("users")
        user_data = await user_collection.find_one({"_id": ObjectId(payload['sub'])})
        if user_data['role'] not in self.roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        return User(**user_data)