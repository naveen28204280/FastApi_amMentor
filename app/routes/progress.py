from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from pathlib import Path
from filelock import FileLock

router = APIRouter()

STORAGE_PATH = Path("/mnt/storage")

PROGRESS_FILE = STORAGE_PATH / "progress.json"
LOCK_FILE = PROGRESS_FILE.with_suffix(".lock")
USERS_FILE = Path(__file__).parent.parent / "static" / "users.json"
MENTORSHIP_FILE = Path(__file__).parent.parent / "static" / "mentorship.json"


class TaskSubmission(BaseModel):
    mentee_email: str
    track_id: str
    task_no: int
    reference_link: str

class TaskApproval(BaseModel):
    mentor_email: str
    mentee_email: str
    track_id: str
    task_no: int
    status: str  # approved/paused/rejected
    mentor_feedback: str | None = None

@router.post("/submit-task")
def submit_task(data: TaskSubmission):
    with FileLock(str(LOCK_FILE)):
        progress = []
        if PROGRESS_FILE.exists():
            try:
                with open(PROGRESS_FILE, "r") as f:
                    progress = json.load(f)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="progress.json is malformed")
        for p in progress:
            if (
                p["mentee_email"] == data.mentee_email and 
                p["track_id"] == data.track_id and 
                p["task_no"] == data.task_no
            ):
                raise HTTPException(status_code=400, detail="Task already submitted")
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Malformed users.json")
        user = next((u for u in users if u["email"] == data.mentee_email), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found in users.json")
        mentee_name = user["name"]
        entry = {
            "mentee_email": data.mentee_email,
            "mentee_name": mentee_name,
            "track_id": data.track_id,
            "task_no": data.task_no,
            "reference_link": data.reference_link,
            "status": "submitted",
            "submitted_at": datetime.now().isoformat(),
            "mentor_feedback": None,
            "approved_at": None
        }
        progress.append(entry)
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
        return {"message": "Task submitted successfully", "entry": entry}
@router.patch("/approve-task")
def approve_task(data: TaskApproval):
    if not MENTORSHIP_FILE.exists():
        raise HTTPException(status_code=500, detail="Mentorship mapping not found")
    with open(MENTORSHIP_FILE, "r") as f:
        mapping = json.load(f)
    mentor_entry = next((m for m in mapping if m["mentor_email"] == data.mentor_email), None)
    if not mentor_entry:
        raise HTTPException(status_code=403, detail="Mentor not assigned to any mentees")
    if data.mentee_email not in mentor_entry["mentees"]:
        raise HTTPException(status_code=403, detail="Mentor not authorized to review this mentee")
    with FileLock(str(LOCK_FILE)):
        if not PROGRESS_FILE.exists():
            raise HTTPException(status_code=404, detail="No submissions found")
        try:
            with open(PROGRESS_FILE, "r") as f:
                progress = json.load(f)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Malformed progress.json")
        task_found = False
        for i, entry in enumerate(progress):
            if (
                entry["mentee_email"] == data.mentee_email and
                entry["track_id"] == data.track_id and
                entry["task_no"] == data.task_no
            ):
                task_found = True
                progress[i]["status"] = data.status
                progress[i]["mentor_feedback"] = data.mentor_feedback
                if data.status == "approved":
                    progress[i]["approved_at"] = datetime.now().isoformat()
                break
        if not task_found:
            raise HTTPException(status_code=404, detail="Submission not found")

        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
        return {"message": f"Task {data.status}", "entry": progress[i]}