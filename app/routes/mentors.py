from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()

MENTORSHIP_FILE = Path(__file__).parent.parent / "static" / "mentorship.json"

@router.get("/mentees/{mentor_email}")
def get_mentees_for_mentor(mentor_email: str):
    if not MENTORSHIP_FILE.exists():
        raise HTTPException(status_code=404, detail="Mapping not found")

    try:
        with open(MENTORSHIP_FILE, "r") as f:
            mentorship = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Malformed mentorship.json")

    mentor_entry = next((m for m in mentorship if m["mentor_email"] == mentor_email), None)

    if not mentor_entry:
        raise HTTPException(status_code=404, detail="Mentor not mapped to any mentees")

    return {
        "mentor_email": mentor_email,
        "mentees": mentor_entry["mentees"]
    }