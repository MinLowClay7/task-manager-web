# importaciones necesarias para funciones CRUD relacionadas con usuarios y autenticación
from sqlalchemy.orm import Session
from app import models, schemas
from app.repositories.users import get_user_by_email
from app.core.security import get_password_hash, verify_password

# Función para crear un nuevo usuario
def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_password = get_password_hash(user_in.password)

    user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Función para autenticar un usuario con email y contraseña
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
