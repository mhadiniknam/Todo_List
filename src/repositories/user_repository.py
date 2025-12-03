from sqlalchemy.orm import Session
from models.user import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for all data access logic related to Users.
    """
    def __init__(self, db_session: Session):
        super().__init__(model=User, db_session=db_session)

    def get_by_username(self, username: str) -> User:
        """
        Get a user by username.
        """
        return self.db_session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        """
        Get a user by email.
        """
        return self.db_session.query(User).filter(User.email == email).first()