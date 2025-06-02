from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random, string

from app.db import models, crud
from app.db.db import get_db
from app.schemas.user import UserCreate, UserOut
from app.utils.mail import send_email

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        email=user.email,
        name=user.name,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get("/send-otp/{email}")
def send_otp(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_code = ''.join(random.choices(string.digits, k=4))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    crud.create_or_update_otp(db, email, otp_code, expiry)
    send_email(email, otp_code)

    return {"message": f"OTP sent to {email}"}
@router.get("/verify-otp/{email}", response_model=UserOut)
def verify_otp(email: str, otp: str = Query(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_entry = crud.get_otp_by_email(db, email)
    if not otp_entry or otp_entry.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    db.delete(otp_entry)
    db.commit()

    return user

@router.get("/user/{email}", response_model=UserOut)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user