import os
from dotenv import load_dotenv
from repositories.project_repository import ProjectRepository
from models.project import Project
from exceptions.service_exceptions import (
    ProjectLimitReachedError, 
    ProjectNameExistsError, 
    ProjectNotFoundError, 
    EmptyTitleError, 
    TitleTooLongError, 
    DescriptionTooLongError
)

load_dotenv() 
MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 2))

class ProjectService:
    """
    The service layer for handling all business logic related to projects.
    """
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def create_project(self, data: dict) -> Project:
        """
        Creates a new project after validating all business rules.
        """
        name = data.get("name")
        
        # --- Validation Logic from SimpleStorage ---
        if not name or len(name.strip()) == 0:
            raise EmptyTitleError("Project name cannot be empty.")
        if len(name) > 30:
            raise TitleTooLongError("Project name cannot be more than 30 characters.")
        if len(data.get("description", "")) > 150:
            raise DescriptionTooLongError("Project description cannot be more than 150 characters.")

        # To check for duplicates, we must list all projects and check in Python
        # (This is a direct result of the minimal repository design)
        all_projects = self.project_repository.list()
        if any(p.name == name for p in all_projects):
            raise ProjectNameExistsError(f"A project with the name '{name}' already exists.")

        if len(all_projects) >= MAX_NUMBER_OF_PROJECT:
            raise ProjectLimitReachedError(f"Maximum number of projects ({MAX_NUMBER_OF_PROJECT}) reached.")
        # --- End of Validation Logic ---

        # If all rules pass, ask the repository to add the project
        return self.project_repository.add(data)

    def edit_project(self, project_id: int, update_data: dict) -> Project:
        """
        Edits an existing project's attributes after validation.
        """
        # First, get the object to edit
        project = self.project_repository.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

        new_name = update_data.get("name")
        new_description = update_data.get("description")

        # --- Validation Logic from SimpleStorage ---
        if not new_name or len(new_name.strip()) == 0:
            raise EmptyTitleError("New project name cannot be empty.")
        if len(new_name) > 30:
            raise TitleTooLongError("New project name cannot be more than 30 characters.")
        if new_description and len(new_description) > 150:
            raise DescriptionTooLongError("New description cannot be more than 150 characters.")

        # Check if another project (with a different ID) already has the new name
        all_projects = self.project_repository.list()
        if any(p.name == new_name and p.id != project_id for p in all_projects):
            raise ProjectNameExistsError(f"Another project with the name '{new_name}' already exists.")
        # --- End of Validation Logic ---
        
        # Directly modify the SQLAlchemy model object.
        # The session will track this change. We do NOT call a repo.update() method.
        project.name = new_name
        project.description = new_description
        
        return project

    def delete_project(self, project_id: int) -> Project:
        """Deletes a project."""
        deleted_project = self.project_repository.delete(project_id)
        if not deleted_project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        return deleted_project

    def list_projects(self) -> list[Project]:
        """Returns a list of all projects."""
        return self.project_repository.list()