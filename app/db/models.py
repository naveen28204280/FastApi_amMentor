from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "mentor" or "mentee"

class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(Text)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    task_no = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    points = Column(Integer, default=10)
    deadline_days = Column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint("track_id", "task_no", name="unique_track_task"),)

    track = relationship("Track", back_populates="tasks")

Track.tasks = relationship("Task", back_populates="track", cascade="all, delete-orphan")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    mentee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    reference_link = Column(Text, nullable=False)
    status = Column(String, default="submitted")  # submitted / approved / paused / rejected
    submitted_at = Column(DateTime, default=datetime.utcnow)
    start_date = Column(DateTime, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    mentor_feedback = Column(Text, nullable=True)
    mentee = relationship("User")
    task = relationship("Task")

class MentorMenteeMap(Base):
    __tablename__ = "mentor_mentee_map"
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentee_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (UniqueConstraint("mentor_id", "mentee_id", name="unique_mentor_mentee"),)

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"))
    mentee_id = Column(Integer, ForeignKey("users.id"))
    total_points = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
class OTP(Base):
    __tablename__ = "otp"

    email = Column(String, primary_key=True, index=True)
    otp = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)