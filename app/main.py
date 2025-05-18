from fastapi import FastAPI
from app.routes import auth 
from app.routes import tracks

app = FastAPI(title="amMentor API")

app.include_router(auth.router) 
app.include_router(tracks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to amMentor Backend"}