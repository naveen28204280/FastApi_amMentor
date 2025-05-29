from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.db.db import get_db
from app.schemas.track import TrackOut
from app.schemas.task import TaskOut
from app.db import crud

router = APIRouter()

@router.get("/", response_model=list[TrackOut])
def list_tracks(db: Session = Depends(get_db)):
    return db.query(models.Track).all()

@router.get("/{track_id}/tasks", response_model=list[TaskOut])
def list_tasks_for_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(models.Track).filter_by(id=track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    tasks = db.query(models.Task).filter_by(track_id=track_id).order_by(models.Task.task_no).all()
    tasks_with_status={}
    for task in tasks:
        submission_of_task = db.query(models.Submission).filter_by(id=task.id).first()
        if submission_of_task:
            task['status'] = submission_of_task.status
            task['time_spent'] = crud.find_time_spent_on_task(submission_of_task.id)
        else:
            task['status'] = "Not started"
            task['time_spent'] = 0
        tasks_with_status.append(task)
    return tasks_with_status