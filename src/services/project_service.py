import os
from dotenv import load_dotenv
from repositories.project_repository import ProjectRepository
from models.project import Project

# Load environment variables from the .env file in the project root
load_dotenv() 

# Get the max number of projects from the environment and convert it to an integer
MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 2))

class ProjectService:
    """
    The service layer for handling business logic related to projects.
    """
    def __init__(self, project_repository: ProjectRepository):
        """
        Initializes the service with a project repository.
        This is an example of Dependency Injection.
        """
        self.project_repository = project_repository

    def create_project(self, name: str, description: str) -> Project:
        """
        Creates a new project after validating business rules.
        """
        # --- Start of Business Logic ---
        # Rule 1: Check if the maximum number of projects has been reached.
        project_count = self.project_repository.count() # We will add this method next
        if project_count >= MAX_NUMBER_OF_PROJECT:
            raise ValueError(f"Maximum number of projects ({MAX_NUMBER_OF_PROJECT}) reached.")

        # Rule 2: You could add other rules, like checking for duplicate names.
        # --- End of Business Logic ---

        # If all rules pass, tell the repository to create the project.
        new_project_data = {"name": name, "description": description}
        created_project = self.project_repository.create(new_project_data)

        return created_project

    def get_all_projects(self) -> list[Project]:
        """Gets all projects. This is a simple pass-through to the repository."""
        return self.project_repository.get_all()