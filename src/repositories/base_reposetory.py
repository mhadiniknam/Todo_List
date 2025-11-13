from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session
from db.base import Base

# This is the generic type that we can pass the Project or Task Models in it (It's generic like C++ generic type)
# That used for type hinting which is crucial in this project
ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    A generic repository with basic CRUD (Create, Read, Update, Delete) operations.
    """
    def __init__(self, model: Type[ModelType], db_session: Session):
        """
        Initializes the repository with the database session and the model type.

        :param model: The SQLAlchemy model class (e.g., Project, Task).
        :param db_session: The SQLAlchemy Session object for database communication.
        """
        self.model = model
        self.db_session = db_session

    def get_by_id(self, item_id: int) -> ModelType | None:
        """Fetches a single record by its primary key."""
        return self.db_session.query(self.model).filter(self.model.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Fetches all records with optional pagination."""
        return self.db_session.query(self.model).offset(skip).limit(limit).all()

    def create(self, data: dict) -> ModelType:
        """Creates a new record in the database."""
        db_item = self.model(**data)
        self.db_session.add(db_item)
        self.db_session.commit()
        self.db_session.refresh(db_item)
        return db_item