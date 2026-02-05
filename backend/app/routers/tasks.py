from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
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

    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),

    order_by: str = Query("created_at"),
    order: str = Query("desc"),

    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    # filtros
    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    if search:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))

    # columnas permitidas
    order_columns = {
        "created_at": models.Task.created_at,
        "title": models.Task.title,
        "completed": models.Task.completed,
    }

    if order_by not in order_columns:
        raise HTTPException(status_code=400, detail="Invalid order_by field")

    column = order_columns[order_by]

    if order == "asc":
        query = query.order_by(asc(column))
    elif order == "desc":
        query = query.order_by(desc(column))
    else:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")

    return query.offset(offset).limit(limit).all()


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


@router.put("/{task_id}", response_model=schemas.Task)
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


