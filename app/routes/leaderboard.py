from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.db import models, crud
from app.utils.helpers import format_leaderboard_entry

router = APIRouter()

@router.get("/{track_id}")
def get_leaderboard(track_id: int, db: Session = Depends(get_db)):
    track = db.query(models.Track).filter_by(id=track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    raw_entries = crud.get_leaderboard_data(db, track_id=track_id)

    leaderboard = [
        format_leaderboard_entry(name, total_points, tasks_completed)
        for name, total_points, tasks_completed in raw_entries
    ]

    return {
        "track_id": track_id,
        "track_title": track.title,
        "leaderboard": leaderboard
    }