import os
import datetime
from dotenv import load_dotenv
from repositories.task_repository import TaskRepository
from repositories.project_repository import ProjectRepository
from models.task import Task

load_dotenv()
MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK", 10))
VALID_STATUSES = {"todo", "doing", "done"}

class TaskService:
    """
    The service layer for handling all business logic related to tasks.
    """
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository):
        self.task_repository = task_repository
        self.project_repository = project_repository

    def create_task(self, data: dict) -> Task:
        """Creates a new task for a project after validation."""
        project_id = data.get("project_id")
        status = data.get("status", "todo")
        title = data.get("title", "")
        deadline_str = data.get("deadline")

        # --- Validation Logic from SimpleStorage ---
        if self.project_repository.get(project_id) is None:
            raise ValueError(f"Project with ID {project_id} does not exist.")

        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one of: {VALID_STATUSES}")
        
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty.")

        # Validate deadline format
        if deadline_str:
            try:
                datetime.datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Deadline must be in YYYY-MM-DD format.")

        # Use the efficient repository method to check the task limit
        tasks_in_project = self.task_repository.list_for_project(project_id)
        if len(tasks_in_project) >= MAX_NUMBER_OF_TASK:
            raise ValueError(f"Project {project_id} has reached its task limit ({MAX_NUMBER_OF_TASK}).")
        # --- End of Validation Logic ---

        return self.task_repository.add(data)

    def edit_task(self, task_id: int, update_data: dict) -> Task:
        """Edits an existing task."""
        task = self.task_repository.get(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")

        # --- Validation ---
        new_title = update_data.get("title")
        new_status = update_data.get("status")
        new_deadline_str = update_data.get("deadline")

        if not new_title or len(new_title.strip()) == 0:
            raise ValueError("New title cannot be empty.")
        if len(new_title) > 30:
            raise ValueError("Task title cannot be more than 30 characters.")
        if len(update_data.get("description", "")) > 150:
            raise ValueError("Task description cannot be more than 150 characters.")
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Must be one of: {VALID_STATUSES}")
        if new_deadline_str:
            try:
                datetime.datetime.strptime(new_deadline_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("New deadline must be in YYYY-MM-DD format.")
        # --- End of Validation ---

        # Directly modify the model object
        task.title = new_title
        task.description = update_data.get("description")
        task.deadline = new_deadline_str
        task.status = new_status
        
        return task
    
    def delete_task(self, task_id: int) -> Task:
        """Deletes a task."""
        deleted_task = self.task_repository.delete(task_id)
        if not deleted_task:
            raise ValueError(f"Task with ID {task_id} not found.")
        return deleted_task

    def list_tasks_for_project(self, project_id: int) -> list[Task]:
        """Lists all tasks for a given project."""
        if self.project_repository.get(project_id) is None:
            raise ValueError(f"Project with ID {project_id} does not exist.")
        return self.task_repository.list_for_project(project_id)

    def close_all_overdue_tasks(self) -> list[Task]:
        """
        Finds all tasks across all projects that are past their deadline and 
        are not yet 'done'. It updates their status to 'done'.

        This is a batch operation intended for a scheduled job.

        :return: A list of the tasks that were just closed.
        """
        today = datetime.date.today()
        closed_tasks = []

        all_tasks = self.task_repository.list()

        for task in all_tasks:
            if task.status == "done" or not task.deadline:
                continue

            try:
                deadline_date = datetime.datetime.strptime(task.deadline, "%Y-%m-%d").date()
                if deadline_date < today:
                    task.status = "done"
                    closed_tasks.append(task)
            except (ValueError, TypeError):
                continue
        
        return closed_tasks