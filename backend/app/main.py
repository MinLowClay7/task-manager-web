from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import tasks

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(tasks.router)