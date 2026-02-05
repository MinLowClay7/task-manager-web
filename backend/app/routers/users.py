from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.crud import users as crud_users
from app.database import get_db

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
