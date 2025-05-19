from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.db.db import get_db

router = APIRouter()

@router.get("/{mentor_email}/mentees")
def get_mentees_for_mentor(mentor_email: str, db: Session = Depends(get_db)):
    mentor = db.query(models.User).filter_by(email=mentor_email, role="mentor").first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    mapping = db.query(models.MentorMenteeMap).filter_by(mentor_id=mentor.id).all()
    mentee_ids = [m.mentee_id for m in mapping]

    if not mentee_ids:
        return {"mentor_email": mentor_email, "mentees": []}

    mentees = db.query(models.User).filter(models.User.id.in_(mentee_ids)).all()

    return {
        "mentor_email": mentor.email,
        "mentees": [{"name": m.name, "email": m.email} for m in mentees]
    }