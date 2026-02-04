from sqlalchemy.orm import Session
from app import models

def get_tasks(db: Session):
    return db.query(models.Task).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db: Session, task):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task
