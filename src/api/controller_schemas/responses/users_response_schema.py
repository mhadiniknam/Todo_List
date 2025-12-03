from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
    """
    Schema for user response data
    """
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    """
    Schema for user login response
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse