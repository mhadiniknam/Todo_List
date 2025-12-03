from models.user import User
from passlib.context import CryptContext
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    The service layer for handling all business logic related to users.
    """
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, data: dict) -> User:
        """Creates a new user after validation and password hashing."""
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Validate input
        if not username or len(username.strip()) == 0:
            raise ValueError("Username cannot be empty.")
        if not email or len(email.strip()) == 0:
            raise ValueError("Email cannot be empty.")
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        # Check if username or email already exists
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError(f"Username '{username}' already exists.")

        existing_email = self.user_repository.get_by_email(email)
        if existing_email:
            raise ValueError(f"Email '{email}' already exists.")

        # Hash the password
        hashed_password = pwd_context.hash(password)
        data["hashed_password"] = hashed_password
        
        # Remove plain password from data to avoid accidentally storing it
        if "password" in data:
            del data["password"]

        return self.user_repository.add(data)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user by username and password."""
        user = self.user_repository.get_by_username(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.user_repository.get(user_id)

    def update_user(self, user_id: int, update_data: dict) -> User:
        """Update a user."""
        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        # Update the user fields
        for field, value in update_data.items():
            if value is not None:
                if field == "password":
                    # If password is being updated, hash it
                    setattr(user, "hashed_password", pwd_context.hash(value))
                else:
                    setattr(user, field, value)

        return user

    def delete_user(self, user_id: int) -> User:
        """Delete a user."""
        deleted_user = self.user_repository.delete(user_id)
        if not deleted_user:
            raise ValueError(f"User with ID {user_id} not found.")
        return deleted_user