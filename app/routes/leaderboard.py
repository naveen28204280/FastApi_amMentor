from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from collections import defaultdict

router = APIRouter()

PROGRESS_FILE = Path(__file__).parent.parent / "static" / "progress.json"
TASKS_FOLDER = Path(__file__).parent.parent / "static" / "tasks"

@router.get("/leaderboard/{track_id}")
def get_leaderboard(track_id: str):
    if not PROGRESS_FILE.exists():
        raise HTTPException(status_code=404, detail="No progress data found")
    try:
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Malformed progress.json")
    task_file = TASKS_FOLDER / f"{track_id}.json"
    if not task_file.exists():
        raise HTTPException(status_code=404, detail="Track not found")
    with open(task_file, "r") as f:
        tasks = json.load(f)
    task_points = {task["task_no"]: task["points"] for task in tasks}
    leaderboard = defaultdict(lambda: {
        "mentee_name": None,
        "total_points": 0,
        "tasks_completed": 0
    })
    for entry in progress:
        if entry["track_id"] == track_id and entry["status"] == "approved":
            email = entry["mentee_email"]
            name = entry.get("mentee_name", email)
            task_no = entry["task_no"]
            points = task_points.get(task_no, 0)
            leaderboard[email]["mentee_name"] = name
            leaderboard[email]["total_points"] += points
            leaderboard[email]["tasks_completed"] += 1
    ranked = sorted(
        [
            {"mentee_email": email, **info}
            for email, info in leaderboard.items()
        ],
        key=lambda x: (-x["total_points"], -x["tasks_completed"])
    )
    return {
        "track": track_id,
        "leaderboard": ranked
    }