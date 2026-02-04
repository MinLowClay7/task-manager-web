from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.crud import tasks as crud_tasks

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/", response_model=list[schemas.tasks.Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud_tasks.get_tasks(db)

@router.post("/", response_model=schemas.tasks.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.tasks.TaskCreate, db: Session = Depends(get_db)):
    return crud_tasks.create_task(db, task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud_tasks.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/{task_id}", response_model=schemas.tasks.Task)
def update_task(
    task_id: int,
    task: schemas.tasks.TaskUpdate,
    db: Session = Depends(get_db)
):
    updated_task = crud_tasks.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

