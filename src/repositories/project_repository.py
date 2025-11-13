from sqlalchemy.orm import Session
from models.project import Project
from repositories.base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    """
    Repository for all database operations related to the Project model.
    """
    def __init__(self, db_session: Session):
        # The 'super()' call initializes the BaseRepository with the Project model
        # and the database session.
        super().__init__(model=Project, db_session=db_session)

    # We are going to add project-specific methods here later if needed.
    # For example:
    # def find_by_name(self, name: str) -> Project | None:
    #     return self.db_session.query(Project).filter(Project.name == name).first()