# app/routers/emergencias.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(
    prefix="/incidente_emergencia",
    tags=["Emergencias"],
)


@router.post("/", response_model=schemas.IncidenteEmergenciaInDB)
def create_incidente(
    incidente: schemas.IncidenteEmergenciaCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Reporta un nuevo incidente o emergencia.
    """
    # Forzamos la asociación con el usuario autenticado
    incidente.id_usuario = current_user.id_usuario
    return crud.create_incidente(db=db, incidente=incidente)


@router.get("/{incidente_id}", response_model=schemas.IncidenteEmergenciaInDB)
def read_incidente(
    incidente_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene los detalles de un incidente específico.
    Solo el usuario que lo reportó o un administrador pueden verlo.
    """
    db_incidente = crud.get_incidente(db, incidente_id)
    if not db_incidente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incidente no encontrado."
        )

    if not current_user.es_admin and current_user.id_usuario != db_incidente.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este incidente."
        )

    return db_incidente
