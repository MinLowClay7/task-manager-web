from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import schemas, models
from app.crud import tasks as crud_tasks

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.get("/", response_model=list[schemas.Task])
def get_tasks(
    completed: Optional[bool] = Query(None),
    search: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    if search:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))

    return query.all()

@router.post("/", response_model=schemas.tasks.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.tasks.TaskCreate, db: Session = Depends(get_db)):
    return crud_tasks.create_task(db, task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()


@router.patch("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


