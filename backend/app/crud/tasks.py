# importaciones necesarias
from sqlalchemy.orm import Session
from app import models, schemas

# funciones CRUD para tareas
def get_task(
        db: Session, 
        task_id: int
        ):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(
        db: Session,
        limit: int = None,
        offset: int = 0
        ):
    query = db.query(models.Task)
    if limit is not None:
        query = query.limit(limit)
    return query.offset(offset).all()

def get_tasks_by_user(
        db: Session, 
        user_id: int, 
        limit: int = None, 
        offset: int = 0
        ):
    return (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id)
        .offset(offset)
        .limit(limit)
        .all()
    )

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(
        **task.model_dump(),
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == user_id)
        .first()
    )
    if not task:
        return None

    db.delete(task)
    db.commit()
    return task

def update_task(db: Session, task_id: int, user_id: int, task_in: schemas.TaskUpdate):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == user_id)
        .first()
    )
    if not task:
        return None

    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task
