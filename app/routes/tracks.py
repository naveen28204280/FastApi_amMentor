from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()

BASE_PATH = Path(__file__).parent.parent / "static"
TRACKS_FILE = BASE_PATH / "tracks.json"
TASKS_FOLDER = BASE_PATH / "tasks"

@router.get("/tracks")
def get_tracks():
    with open(TRACKS_FILE, "r") as f:
        return json.load(f)

@router.get("/track/{track_id}/tasks")
def get_tasks_for_track(track_id: str):
    task_file = TASKS_FOLDER / f"{track_id}.json"
    if not task_file.exists():
        raise HTTPException(status_code=404, detail="Track not found")
    
    with open(task_file, "r") as f:
        return json.load(f)