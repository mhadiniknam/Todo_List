import os
from dotenv import load_dotenv
from repositories.task_repository import TaskRepository
from repositories.project_repository import ProjectRepository
from models.task import Task

load_dotenv()
MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK", 10))

class TaskService:
    """
    The service layer for handling business logic related to tasks.
    """
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository):
        """Initializes the service with necessary repositories."""
        self.task_repository = task_repository
        self.project_repository = project_repository

    def create_task(self, title: str, project_id: int) -> Task:
        """
        Creates a new task for a given project after validating business rules.
        """
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} does not exist.")

        tasks_in_project_count = self.task_repository.count_by_project(project_id) # We'll add this next
        if tasks_in_project_count >= MAX_NUMBER_OF_TASK:
            raise ValueError(f"Project {project_id} has reached its maximum number of tasks ({MAX_NUMBER_OF_TASK}).")

        new_task_data = {"title": title, "project_id": project_id}
        created_task = self.task_repository.create(new_task_data)
        return created_task

    def get_tasks_for_project(self, project_id: int) -> list[Task]:
        """Gets all tasks for a specific project."""
        return self.task_repository.get_all_for_project(project_id)

    def count_by_project(self, project_id: int) -> int:
        """Counts the number of tasks associated with a specific project."""
        return self.db_session.query(Task).filter(Task.project_id == project_id).count()

    def get_all_for_project(self, project_id: int) -> list[Task]:
        """Gets all task records associated with a specific project."""
        return self.db_session.query(Task).filter(Task.project_id == project_id).all()

    def get_tasks_for_project(self, project_id: int) -> list[Task]:
        """
        Gets all tasks for a specific project after verifying the project exists.
        """
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} does not exist.")

        return self.task_repository.get_all_for_project(project_id)
