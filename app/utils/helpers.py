from typing import List, Optional
from app.db.models import User

def get_user_id_by_email(users: List[User], email: str) -> Optional[int]:
    for user in users:
        if user.email == email:
            return user.id
    return None

def calculate_total_points(submissions, task_lookup):
    total = 0
    for s in submissions:
        if s.status == "approved":
            total += task_lookup.get(s.task_id, 0)
    return total

def format_leaderboard_entry(name: str, total_points: int, tasks_completed: int) -> dict:
    return {
        "mentee_name": name,
        "total_points": total_points,
        "tasks_completed": tasks_completed
    }