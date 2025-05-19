from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    track_id: int
    task_no: int
    title: str
    description: Optional[str] = None
    points: int = 10
    deadline: Optional[datetime] = None 

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True