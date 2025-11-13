from sqlalchemy.orm import Session
from models.task import Task
from repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    """
    Repository for all database operations related to the Task model.
    """
    def __init__(self, db_session: Session):
        # The 'super()' call initializes the BaseRepository with the Task model
        # and the database session.
        super().__init__(model=Task, db_session=db_session)

    # We can add task-specific methods here later if needed.
    # For example:
    # def find_by_status(self, status: str) -> list[Task]:
    #     return self.db_session.query(Task).filter(Task.status == status).all()