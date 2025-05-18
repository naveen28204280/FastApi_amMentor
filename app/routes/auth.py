from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

router = APIRouter()

STATIC_PATH = Path(__file__).parent.parent / "static" / "users.json"

class LoginRequest(BaseModel):
    email: str

@router.post("/login")
def login_user(data: LoginRequest):
    with open(STATIC_PATH, "r") as f:
        users = json.load(f)
    
    user = next((u for u in users if u["email"].lower() == data.email.lower()), None)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email")

    return {
        "message": f"Login successful for {user['name']}",
        "role": user["role"],
        "user": user
    }