from typing import Dict, List
from ..Task.Task import Task
from ..project.project import project

class SimpleStorage:
    """
    Simple in-memory storage using a dictionary.
    Key: project name
    Value: list of tasks
    """
    def __init__(self):
        self._projects: Dict[project, List[Task]] = {}
    