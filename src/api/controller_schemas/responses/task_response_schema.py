from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskResponse(BaseModel):
    """
    Schema for task response data
    """
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    project_id: int
    
    class Config:
        from_attributes = True