# main del backend, punto de entrada de la aplicación
from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import tasks, users, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Incluimos los routers de las diferentes partes de la aplicación
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

# Endpoint de prueba para verificar que la aplicación está funcionando
@app.get("/")
def root():
    return {"status": "ok"}
