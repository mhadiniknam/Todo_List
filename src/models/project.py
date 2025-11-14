from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # This establishes the "one-to-many" relationship. It actually have casacde feature and use to build a connection
    # between project and Tasket 
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
