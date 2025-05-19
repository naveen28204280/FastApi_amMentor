from pydantic import BaseModel
from typing import Optional

class TrackBase(BaseModel):
    title: str
    description: Optional[str] = None

class TrackCreate(TrackBase):
    pass

class TrackOut(TrackBase):
    id: int

    class Config:
        orm_mode = True