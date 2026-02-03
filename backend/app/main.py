from fastapi import FastAPI
from .database import Base, engine
from .routers import tasks

app = FastAPI()
app.include_router(tasks.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok"}