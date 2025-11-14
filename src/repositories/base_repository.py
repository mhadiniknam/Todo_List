from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session
from db.base import Base

# Create a generic TypeVar for our SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    A generic, collection-oriented repository with minimal CRUD operations.
    It does NOT commit the session.
    """
    def __init__(self, model: Type[ModelType], db_session: Session):
        """
        Initializes the repository.

        :param model: The SQLAlchemy model class.
        :param db_session: The SQLAlchemy Session for database communication.
        """
        self.model = model
        self.db_session = db_session

    def add(self, data: dict) -> ModelType:
        """
        Creates a new model instance from a dictionary and adds it to the session.
        """
        db_item = self.model(**data)
        self.db_session.add(db_item)
        self.db_session.flush() # Flushes to get the ID, but does not commit
        self.db_session.refresh(db_item)
        return db_item

    def get(self, item_id: int) -> ModelType | None:
        """Fetches a single record by its primary key."""
        return self.db_session.query(self.model).filter(self.model.id == item_id).first()

    def list(self) -> list[ModelType]:
        """Fetches all records."""
        return self.db_session.query(self.model).all()
    
    def delete(self, item_id: int) -> ModelType | None:
        """Deletes a record by its primary key."""
        item = self.get(item_id)
        if item:
            self.db_session.delete(item)
            self.db_session.flush() # Flushes the delete, but does not commit
        return item