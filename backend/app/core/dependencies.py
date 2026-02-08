# importaciones necesarias
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models import User

# Configuración de seguridad y autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Función para obtener el usuario actual a partir del token JWT
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401)
    return user

# Función para obtener un usuario por email (usada en autenticación)
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()