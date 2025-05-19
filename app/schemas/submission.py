from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubmissionBase(BaseModel):
    track_id: int
    task_no: int
    reference_link: str

class SubmissionCreate(SubmissionBase):
    mentee_email: str

class SubmissionOut(BaseModel):
    id: int
    mentee_id: int
    task_id: int
    reference_link: str
    status: str
    submitted_at: datetime
    approved_at: Optional[datetime] = None
    mentor_feedback: Optional[str] = None

    class Config:
        orm_mode = True

class SubmissionApproval(BaseModel):
    submission_id: int
    mentor_email: str
    status: str  # approved, paused, rejected
    mentor_feedback: Optional[str] = None