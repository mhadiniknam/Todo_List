"""
API Router for the Todo List Application

This module defines the API endpoints that map to the existing CLI functionality.
Each endpoint corresponds to a command that was previously available in the CLI parser.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db_session
from models.project import Project
from models.task import Task
from services.project_service import ProjectService
from services.task_service import TaskService
from api.controller_schemas.responses.project_response_schema import ProjectResponse
from api.controller_schemas.responses.task_response_schema import TaskResponse

router = APIRouter()

def get_project_service(db: Session = Depends(get_db_session)) -> ProjectService:
    """Dependency to get project service instance with repository"""
    from repositories.project_repository import ProjectRepository
    project_repo = ProjectRepository(db)
    return ProjectService(project_repo)


def get_task_service(db: Session = Depends(get_db_session)) -> TaskService:
    """Dependency to get task service instance with repositories"""
    from repositories.task_repository import TaskRepository
    from repositories.project_repository import ProjectRepository
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    return TaskService(task_repo, project_repo)


# Project Management Endpoints
# Corresponds to CLI command: create-project <name> <description>
@router.post("/projects", response_model=ProjectResponse)
def create_project(
    name: str,
    description: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Create a new project with name and description
    CLI equivalent: create-project <name> <description>
    """
    data = {
        "name": name,
        "description": description
    }
    return project_service.create_project(data)


# Corresponds to CLI command: list-projects
@router.get("/projects", response_model=List[ProjectResponse])
def list_projects(
    project_service: ProjectService = Depends(get_project_service)
):
    """
    List all projects
    CLI equivalent: list-projects
    """
    return project_service.list_projects()


# Corresponds to CLI command: edit-project <id> <new_name> <new_desc>
@router.put("/projects/{project_id}", response_model=ProjectResponse)
def edit_project(
    project_id: int,
    name: str,
    description: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Edit an existing project by ID
    CLI equivalent: edit-project <id> <new_name> <new_desc>
    """
    update_data = {
        "name": name,
        "description": description
    }
    return project_service.edit_project(project_id, update_data)


# Corresponds to CLI command: delete-project <id>
@router.delete("/projects/{project_id}", response_model=ProjectResponse)
def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Delete a project by ID
    CLI equivalent: delete-project <id>
    """
    return project_service.delete_project(project_id)


# Task Management Endpoints
# Corresponds to CLI command: create-task <project_id> <title> <description> [deadline YYYY-MM-DD] [status]
@router.post("/tasks", response_model=TaskResponse)
def create_task(
    project_id: int,
    title: str,
    description: str,
    deadline: str = None,
    status: str = "todo",
    task_service: TaskService = Depends(get_task_service)
):
    """
    Create a new task in a project
    CLI equivalent: create-task <project_id> <title> <description> [deadline YYYY-MM-DD] [status]
    """
    data = {
        "project_id": project_id,
        "title": title,
        "description": description,
        "deadline": deadline,
        "status": status
    }
    return task_service.create_task(data)


# Corresponds to CLI command: list-tasks <project_id>
@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def list_tasks_for_project(
    project_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    List all tasks for a specific project
    CLI equivalent: list-tasks <project_id>
    """
    return task_service.list_tasks_for_project(project_id)


# Corresponds to CLI command: edit-task <task_id> <new_title> <new_desc> <new_deadline> <new_status>
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def edit_task(
    task_id: int,
    title: str,
    description: str,
    deadline: str = None,
    status: str = "todo",
    task_service: TaskService = Depends(get_task_service)
):
    """
    Edit an existing task by ID
    CLI equivalent: edit-task <task_id> <new_title> <new_desc> <new_deadline> <new_status>
    """
    update_data = {
        "title": title,
        "description": description,
        "deadline": deadline,
        "status": status
    }
    return task_service.edit_task(task_id, update_data)


# Corresponds to CLI command: delete-task <task_id>
@router.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    Delete a task by ID
    CLI equivalent: delete-task <task_id>
    """
    return task_service.delete_task(task_id)