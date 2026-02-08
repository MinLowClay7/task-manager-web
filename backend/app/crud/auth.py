# Funciones CRUD relacionadas con autenticación y usuarios
from sqlalchemy.orm import Session
from app.models import User
from app.core.security import verify_password

# Función para autenticar un usuario con email y contraseña
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
