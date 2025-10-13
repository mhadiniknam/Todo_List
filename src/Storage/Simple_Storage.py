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
    
    def create_project(self,name : str , desc_name : str):

        if len(name.strip) > 30 :
            print(f"❌ Error: The name can not be more than 30 word")
            return False
         
        if len(desc_name.strip) > 150 :
            print(f"❌ Error: The desciption can not be more than 30 word")
            return False
 
        if name in self._projects :
            print(f"❌ Error: choose another name")
            return False
        

        if(len(self._projects) <= self.projects_limit):
            self._projects[name] = []
            print(f"✅ Project '{name}' created successfully.")
            return True

