from fastapi import FastAPI
from app.routes import auth 


app = FastAPI(title="amMentor API")

app.include_router(auth.router) 
@app.get("/")
def read_root():
    return {"message": "Welcome to amMentor Backend"}