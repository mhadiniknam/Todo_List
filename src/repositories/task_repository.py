from sqlalchemy.orm import Session
from models.task import Task
from repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    """
    Repository for all data access logic related to Tasks.
    """
    def __init__(self, db_session: Session):
        super().__init__(model=Task, db_session=db_session)

    def list_for_project(self, project_id: int) -> list[Task]:
        """
        A specific, efficient query to list all tasks for a given project.
        """
        return self.db_session.query(Task).filter(Task.project_id == project_id).all()