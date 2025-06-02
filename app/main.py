from fastapi import FastAPI
from app.db.db import Base, engine
from app.routes import auth, progress, tracks, leaderboard, mentors , submissions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="amMentor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])
app.include_router(tracks.router, prefix="/tracks", tags=["Tracks"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["Leaderboard"])
app.include_router(mentors.router, prefix="/mentors", tags=["Mentors"])
app.include_router(submissions.router, prefix="/submissions", tags=["Submissions"])

@app.get("/")
def root():
    return {"message": "Welcome to amMentor 🚀"}