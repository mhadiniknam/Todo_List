# src/todolist/models/task.py
from datetime import datetime


class Task:
    def __init__(
        self, title: str, description: str, deadline: str = None, status: str = "todo"
    ):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = status  # todo, doing, done
        self.created_at = datetime.now()

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
