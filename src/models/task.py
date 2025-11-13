import enum
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    # This is the foreign key that creates the link to the 'projects' table.
    project_id = Column(Integer, ForeignKey("projects.id"))

    # This establishes the other side of the relationship, linking a Task
    # back to its single Project object.
    project = relationship("Project", back_populates="tasks")
