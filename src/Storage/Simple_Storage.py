from typing import Dict, List
from ..Task.Task import Task
from dotenv import load_dotenv
import os

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

        if len(self._projects) <= self.projects_limit:
            self._projects[name] = {desc_name : []}
            print(f"✅ Project '{name}' created successfully.")
            return True

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
            self._projects[new_name] = {new_desc : []}
            print(f"✅ Project '{prev_name}' updated to '{new_name}' created successfully.")
            return True
        else:
            print(f"❌ Error: the {prev_name} does not exists")

    def delete_project(self, name : str):
        if name in self._projects:
            del self._projects[name]
            print(f"✅ Project '{name}' deleted successfully.")
        else:
            print(f"❌ Error: the {name} does not exists") 

    def add_task(self, project_name: str, title: str, description: str, deadline: str , status: str):
        if project_name not in self._projects:
            print(f"❌ Error: Project '{project_name}' does not exist.")
            return False
        
        if ((status != "todo") and (status != "doing") and ( status != "done") and (status != None )):
            print(f"❌ Error: status could be only todo, doing, done'.")
            return False

        project_data = self._projects[project_name]

        description_key = next(iter(project_data))
        tasks = project_data[description_key]

        if len(tasks) >= self.tasks_limits:
            print(f"❌ Error: Task limit reached for project '{project_name}'.")
            return False

        if status == None :
            new_task = Task(title=title, description=description, deadline=deadline)
        else :
            new_task = Task(title=title, description=description, deadline=deadline,status = status)
        tasks.append(new_task)

        return True
