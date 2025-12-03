from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db_session
from api.controllers.users_controller import UserController
from api.controller_schemas.requests.users_request_schema import UserCreateRequest, UserLoginRequest
from api.controller_schemas.responses.users_response_schema import UserResponse, UserLoginResponse
from models.user import User

router = APIRouter()

def get_user_controller(db: Session = Depends(get_db_session)) -> UserController:
    """Dependency to get user controller instance"""
    return UserController(db)


@router.post("/users/register", response_model=UserResponse)
def register_user(
    user_data: UserCreateRequest,
    user_controller: UserController = Depends(get_user_controller)
):
    """
    Register a new user
    """
    try:
        user_dict = user_data.model_dump()
        user = user_controller.register_user(user_dict)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/users/login", response_model=UserLoginResponse)
def login_user(
    login_data: UserLoginRequest,
    user_controller: UserController = Depends(get_user_controller)
):
    """
    Authenticate user and return access token
    """
    result = user_controller.authenticate_user(login_data.username, login_data.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user, access_token = result
    return UserLoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    user_controller: UserController = Depends(get_user_controller)
):
    """
    Get user by ID
    """
    user = user_controller.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user():
    """
    Update user information
    """
    # Implementation would go here
    pass


@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user():
    """
    Delete a user
    """
    # Implementation would go here
    pass