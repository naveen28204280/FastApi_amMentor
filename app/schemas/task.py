from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    track_id: int
    task_no: int
    title: str
    description: Optional[str] = None
    points: int = 10

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True