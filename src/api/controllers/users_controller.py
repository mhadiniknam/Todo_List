from typing import Optional
from sqlalchemy.orm import Session
from models.user import User
from services.user_service import UserService
from services.auth_service import AuthService
from repositories.user_repository import UserRepository


class UserController:
    """
    Controller for handling user-related operations
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_repository = UserRepository(db_session)
        self.user_service = UserService(self.user_repository)
        self.auth_service = AuthService()

    def register_user(self, user_data: dict) -> User:
        """
        Register a new user
        """
        return self.user_service.create_user(user_data)

    def authenticate_user(self, username: str, password: str) -> Optional[tuple[User, str]]:
        """
        Authenticate a user and return user object with access token
        """
        user = self.user_service.authenticate_user(username, password)
        if not user:
            return None
        
        # Create access token
        token_data = {"sub": user.username, "user_id": user.id}
        access_token = self.auth_service.create_access_token(
            data=token_data
        )
        
        return user, access_token

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        """
        return self.user_service.get_user(user_id)

    def update_user(self, user_id: int, update_data: dict) -> User:
        """
        Update user information
        """
        return self.user_service.update_user(user_id, update_data)

    def delete_user(self, user_id: int) -> User:
        """
        Delete a user
        """
        return self.user_service.delete_user(user_id)