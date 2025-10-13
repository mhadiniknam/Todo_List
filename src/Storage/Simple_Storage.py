from typing import Dict, List
from ..Task.Task import Task
from dotenv import load_dotenv
import os
import datetime

load_dotenv()


class SimpleStorage:
    """
    Simple in-memory storage using a dictionary.
    Key: project name
    Value: list of tasks
    """

    def __init__(self):
        self._projects: Dict[str, Dict[str, List[Task]]] = {}
        self.projects_limit = int(os.getenv("MAX_NUMBER_OF_PROJECT"))
        self.tasks_limits = int(os.getenv("MAX_NUMBER_OF_TASK"))

    def create_project(self, name: str, desc_name: str):

        if len(name.strip()) > 30:
            print(f"❌ Error: The name can not be more than 30 word")
            return False

        if len(desc_name.strip()) > 150:
            print(f"❌ Error: The desciption can not be more than 30 word")
            return False

        if name in self._projects:
            print(f"❌ Error: choose another name")
            return False

        if len(self._projects) < self.projects_limit:
            self._projects[name] = {desc_name: []}
            print(f"✅ Project '{name}' created successfully.")
            return True
        else:
            print(f"❌ Error: You pass the Projects limit")
            return False

    def edit_project(self, prev_name: str, new_name: str, new_desc: str) -> bool:

        if len(new_name.strip()) > 30:
            print(f"❌ Error: The name can not be more than 30 word")
            return False

        if len(new_desc.strip()) > 150:
            print(f"❌ Error: The desciption can not be more than 30 word")
            return False

        if prev_name == new_name:
            print(f"❌ Error: The new and previous name can not be the same")
            return False

        if prev_name in self._projects:
            del self._projects[prev_name]
            self._projects[new_name] = {new_desc: []}
            print(
                f"✅ Project '{prev_name}' updated to '{new_name}' created successfully."
            )
            return True
        else:
            print(f"❌ Error: the {prev_name} does not exists")

    def delete_project(self, name: str):
        if name in self._projects:
            del self._projects[name]
            print(f"✅ Project '{name}' deleted successfully.")
        else:
            print(f"❌ Error: the {name} does not exists")

    def add_task(
        self,
        project_name: str,
        title: str,
        description: str,
        deadline: str,
        status: str,
    ):
        if project_name not in self._projects:
            print(f"❌ Error: Project '{project_name}' does not exist.")
            return False

        if (
            (status != "todo")
            and (status != "doing")
            and (status != "done")
            and (status != None)
        ):
            print(f"❌ Error: status could be only todo, doing, done'.")
            return False

        project_data = self._projects[project_name]

        description_key = next(iter(project_data))
        tasks = project_data[description_key]

        if len(tasks) >= self.tasks_limits:
            print(f"❌ Error: Task limit reached for project '{project_name}'.")
            return False

        if status == None:
            new_task = Task(title=title, description=description, deadline=deadline)
        else:
            new_task = Task(
                title=title, description=description, deadline=deadline, status=status
            )
        print(f"✅ Task '{title}' created .")
        tasks.append(new_task)

        return True

    def update_task_status(
        self, project_name: str, task_title: str, new_status: str
    ) -> bool:
        if project_name not in self._projects:
            print(f"❌ Error: Project '{project_name}' does not exist.")
            return False

        if new_status not in ("todo", "doing", "done"):
            print(
                f"❌ Error: Invalid status '{new_status}'. Must be one of: todo, doing, done."
            )
            return False

        project_data = self._projects[project_name]
        description_key = next(iter(project_data))
        tasks = project_data[description_key]

        # Find the task by title
        for task in tasks:
            if task.title == task_title:
                task.status = new_status
                print(
                    f"✅ Task '{task_title}' status updated to '{new_status}' in project '{project_name}'."
                )
                return True

        print(
            f"❌ Error: Task titled '{task_title}' not found in project '{project_name}'."
        )
        return False

    def edit_task(
        self,
        project_name: str,
        task_title: str,
        new_title: str,
        new_description: str,
        new_deadline: str,
        new_status: str,
    ) -> bool:
        # Validate project exists
        if project_name not in self._projects:
            print(f"❌ Error: Project '{project_name}' does not exist.")
            return False

        # Validate status
        valid_statuses = {"todo", "doing", "done"}
        if new_status not in valid_statuses:
            print(f"❌ Error: status must be one of {valid_statuses}")
            return False

        # Validate length limits
        if len(new_title.strip()) > 30:
            print("❌ Error: Title can not be more than 30 characters.")
            return False

        if len(new_description.strip()) > 150:
            print("❌ Error: Description can not be more than 150 characters.")
            return False

        # Validate deadline format (example: YYYY-MM-DD)
        try:
            datetime.datetime.strptime(new_deadline, "%Y-%m-%d")
        except ValueError:
            print("❌ Error: Deadline must be in YYYY-MM-DD format.")
            return False

        project_data = self._projects[project_name]
        description_key = next(iter(project_data))
        tasks = project_data[description_key]

        # Find task by title
        for task in tasks:
            if task.title == task_title:
                # Update task fields
                task.title = new_title
                task.description = new_description
                task.deadline = new_deadline
                task.status = new_status
                print(f"✅ Task '{task_title}' updated successfully.")
                return True

        print(
            f"❌ Error: Task titled '{task_title}' not found in project '{project_name}'."
        )
        return False

    def delete_task(self, project_name: str, task_title: str) -> bool:
        # Check if project exists
        if project_name not in self._projects:
            print(f"❌ Error: Project '{project_name}' does not exist.")
            return False

        project_data = self._projects[project_name]
        description_key = next(iter(project_data))
        tasks = project_data[description_key]

        # Find and delete task with matching title
        for i, task in enumerate(tasks):
            if task.title == task_title:
                del tasks[i]
                print(
                    f"✅ Task '{task_title}' deleted successfully from project '{project_name}'."
                )
                return True

        print(
            f"❌ Error: Task with title '{task_title}' not found in project '{project_name}'."
        )
        return False

    def list_projects(self):
        if not self._projects:
            print("No projects found.")
            return

        print("Projects List:")
        # Enumerate projects in order of insertion (order of creation)
        for index, (project_name, project_data) in enumerate(
            self._projects.items(), start=1
        ):
            description = next(iter(project_data))  # The description key
            print(f"ID: {index} | Name: {project_name} | Description: {description}")

    def list_tasks(self, project_name: str):
        if project_name not in self._projects:
            print(f"❌ Error: Project '{project_name}' does not exist.")
            return

        project_data = self._projects[project_name]
        description_key = next(iter(project_data))
        tasks = project_data[description_key]

        if not tasks:
            print(f"No tasks found in project '{project_name}'.")
            return

        print(f"Tasks for project '{project_name}':")
        for idx, task in enumerate(tasks, 1):
            print(
                f"ID: {idx} | Title: {task.title} | Status: {task.status} | Deadline: {task.deadline}"
            )
