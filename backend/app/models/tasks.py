# Modelo de tarea para la aplicación de gestión de tareas
#
# Este modelo define la estructura de la tabla "tasks" en la base de datos, 
# con campos para el título, descripción, estado de completado, 
# fecha de creación y relación con el usuario propietario.
#
# Importaciones necesarias para definir el modelo de tarea
from datetime import datetime, UTC
from sqlalchemy import Boolean, Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

# Definición del modelo de tarea
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", back_populates="tasks")