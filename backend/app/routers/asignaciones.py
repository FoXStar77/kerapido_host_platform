from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(
    prefix="/asignaciones",
    tags=["Asignaciones"],
)

@router.post("/", response_model=schemas.AsignacionInDB)
def create_asignacion(
    asignacion: schemas.AsignacionCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Crea una nueva asignación de servicio.
    Solo un administrador puede realizar esta acción.
    """
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear asignaciones."
        )
    return crud.create_asignacion(db=db, asignacion=asignacion)


@router.get("/{asignacion_id}", response_model=schemas.AsignacionInDB)
def read_asignacion(
    asignacion_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene los detalles de una asignación específica.
    Solo el cliente, el conductor o un administrador pueden verla.
    """
    db_asignacion = crud.get_asignacion(db, asignacion_id)
    if not db_asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación no encontrada."
        )

    db_solicitud = crud.get_solicitud(db, db_asignacion.id_solicitud)
    db_cliente = crud.get_cliente(db, db_solicitud.id_cliente)
    db_conductor = crud.get_conductor(db, db_asignacion.id_conductor)
    
    # Verificar permisos
    is_involved_user = (
        current_user.id_usuario == db_cliente.id_usuario or
        current_user.id_usuario == db_conductor.id_usuario
    )

    if not current_user.es_admin and not is_involved_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta asignación."
        )

    return db_asignacion


@router.put("/{asignacion_id}/precio", response_model=schemas.AsignacionInDB)
def update_asignacion_precio(
    asignacion_id: int,
    precio: float,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Actualiza el precio final de una asignación.
    Solo el conductor asignado o un administrador pueden realizar esta acción.
    """
    db_asignacion = crud.get_asignacion(db, asignacion_id)
    if not db_asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación no encontrada."
        )

    db_conductor = crud.get_conductor(db, db_asignacion.id_conductor)

    if not current_user.es_admin and current_user.id_usuario != db_conductor.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar esta asignación."
        )
    
    return crud.update_asignacion_precio(db, asignacion_id, precio)
