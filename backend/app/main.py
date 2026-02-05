from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import tasks, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"status": "ok"}
