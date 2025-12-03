from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreateRequest(BaseModel):
    """
    Schema for user creation requests
    """
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLoginRequest(BaseModel):
    """
    Schema for user login requests
    """
    username: str
    password: str