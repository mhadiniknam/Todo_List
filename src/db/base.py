from sqlalchemy.orm import declarative_base

Base = declarative_base()
# This will be the base for project and task mdoels
from models.project import Project
from models.task import Task