#mongo db models
from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"  

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: Role 
    is_active: bool = True

    class Settings:
        name = "users"        