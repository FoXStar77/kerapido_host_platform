from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(
    prefix="/vehiculos",
    tags=["Vehículos"],
)

@router.post("/", response_model=schemas.VehiculoInDB)
def create_vehiculo_for_conductor(
    vehiculo: schemas.VehiculoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Crea un nuevo vehículo para un conductor.
    Solo el conductor asociado o un administrador pueden realizar esta acción.
    """
    db_conductor = crud.get_conductor(db, vehiculo.id_conductor)
    if not db_conductor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conductor no encontrado."
        )

    # Verificar que el usuario autenticado sea el conductor o un admin
    if not current_user.es_admin and current_user.id_usuario != db_conductor.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para agregar un vehículo a este conductor."
        )

    return crud.create_vehiculo(db=db, vehiculo=vehiculo)


@router.get("/{vehiculo_id}", response_model=schemas.VehiculoInDB)
def read_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene los detalles de un vehículo específico.
    Solo el conductor propietario o un administrador pueden ver la información completa.
    """
    db_vehiculo = crud.get_vehiculo(db, vehiculo_id)
    if not db_vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado."
        )

    db_conductor = crud.get_conductor(db, db_vehiculo.id_conductor)
    if not current_user.es_admin and current_user.id_usuario != db_conductor.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este vehículo."
        )

    return db_vehiculo


@router.get("/conductor/{conductor_id}", response_model=List[schemas.VehiculoInDB])
def read_vehiculos_by_conductor(
    conductor_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene todos los vehículos de un conductor específico.
    Solo el conductor o un administrador pueden acceder a esta lista.
    """
    db_conductor = crud.get_conductor(db, conductor_id)
    if not db_conductor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conductor no encontrado."
        )

    if not current_user.es_admin and current_user.id_usuario != db_conductor.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los vehículos de este conductor."
        )

    return crud.get_vehiculos_by_conductor(db, conductor_id)
