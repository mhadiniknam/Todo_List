from typing import Dict, List
from ..Task.Task import Task
from ..project.project import project
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
        self._projects: Dict[project, List[Task]] = {}
        self.projects_limit = int(os.getenv("MAX_NUMBER_OF_PROJECT"))
        self.tasks_limits = int(os.getenv("MAX_NUMBER_OF_TASK"))
    
    def create_project(self,project_name : str):
        if project_name in self._projects :
            return False
        
        if(len(self._projects) <= self.projects_limit):
            self._projects[project_name] = []
            return True
