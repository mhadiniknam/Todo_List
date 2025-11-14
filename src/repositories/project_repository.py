from sqlalchemy.orm import Session
from models.project import Project
from repositories.base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    """
    Repository for all data access logic related to Projects.
    """
    def __init__(self, db_session: Session):
        # This initializes the BaseRepository with the Project model
        # and the database session, giving it all the basic CRUD methods.
        super().__init__(model=Project, db_session=db_session)