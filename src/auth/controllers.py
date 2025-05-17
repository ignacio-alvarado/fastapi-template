from fastapi import Depends
from pymongo import AsyncMongoClient
from typing import Annotated
from bcrypt import hashpw, checkpw, gensalt 

from config.db import get_db
from user.models import User, Role
from auth.schemas import RegisterRequest, LoginRequest  
from auth.utils.token import create_token, verify_token

async def register_user(user: RegisterRequest, db: Annotated[AsyncMongoClient, Depends(get_db)]) -> str:
    """
    Register a new user.

    Args:
        user (RegisterRequest): The user to register.
        db (AsyncMongoClient): The database connection.
    
    Returns:
        str: The ID of the registered user.
    """
    user = User(**user.dict(), role=Role.user, is_active=False)

    # Check if email or username already exists
    user_collection = db.get_collection("users")
    existing_user = await user_collection.find_one({"$or": [{"email": user.email}, {"username": user.username}]})
    if existing_user:
        raise Exception("Email or username already exists")
    
    # Hash password
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())
    user.password = hashed_password.decode('utf-8')

    # Insert user into database
    try:
        result = await user_collection.insert_one(user.model_dump())
        return result.inserted_id
    except Exception as e:
        raise Exception(f"Failed to register user: {e}")

async def get_token(user: LoginRequest, db: Annotated[AsyncMongoClient, Depends(get_db)]) -> dict:
    """
    Login a user.

    Args:
        user (LoginRequest): The user to login.
        db (AsyncMongoClient): The database connection.
    
    Returns:
        dict: The JWT token and refresh token.
    """
    user_collection = db.get_collection("users")
    user_data = await user_collection.find_one({"username": user.username})

    if not user_data:
        raise Exception("Invalid credentials")
    
    # Check password
    if not checkpw(user.password.encode('utf-8'), user_data['password'].encode('utf-8')):
        raise Exception("Invalid credentials")

    # Create access and refresh tokens
    tokens = create_token(str(user_data['_id']))
    
    return tokens

def refresh_token(token: str) -> dict:
    """
    Refresh a token.
    """
    payload = verify_token(token)
    return create_token(payload['sub'])