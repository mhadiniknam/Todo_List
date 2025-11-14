# This __init__.py file serves as the public entry point for our models.

# Import the Base class that all models depend on.
from db.base import Base

# Import each of your models using a relative import.
# When these lines are executed, each model class will register itself
# with the SQLAlchemy metadata attached to the 'Base' object.
from .project import Project
from .task import Task