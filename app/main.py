from fastapi import FastAPI
from app.db.db import Base, engine
from app.routes import auth, progress, tracks, leaderboard, mentors


app = FastAPI(title="amMentor API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])
app.include_router(tracks.router, prefix="/tracks", tags=["Tracks"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["Leaderboard"])
app.include_router(mentors.router, prefix="/mentors", tags=["Mentors"])


@app.get("/")
def root():
    return {"message": "Welcome to amMentor 🚀"}