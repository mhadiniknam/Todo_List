from pydantic import BaseModel
from typing import Optional


class ProjectResponse(BaseModel):
    """
    Schema for project response data
    """
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True