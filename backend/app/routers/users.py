from app import crud
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.crud import users as crud_users
from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.security import get_current_user
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    db_user = crud_users.get_user_by_email(db, user_in.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return crud_users.create_user(db, user_in)


@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=schemas.Task)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_task(db, task_in)