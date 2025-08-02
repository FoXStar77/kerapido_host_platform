# app/routers/conductores.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(
    prefix="/conductores",
    tags=["Conductores"],
)


@router.post("/", response_model=schemas.ConductorInDB, status_code=201)
def create_conductor(
    conductor: schemas.ConductorCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Crea un nuevo perfil de conductor.
    Requiere rol de administrador.
    """
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear perfiles de conductor."
        )

    db_usuario = crud.get_usuario(db, usuario_id=conductor.id_usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario asociado no encontrado.")

    if db_usuario.conductor:
        raise HTTPException(status_code=409, detail="El usuario ya es conductor.")

    if not db_usuario.es_conductor:
        db_usuario.es_conductor = True
        db.commit()

    return crud.create_conductor(db=db, conductor=conductor)


@router.get("/", response_model=List[schemas.ConductorInDB])
def read_conductores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Lista todos los conductores.
    Acceso exclusivo para administradores.
    """
    if not current_user.es_admin:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder.")
    return crud.get_conductores(db, skip=skip, limit=limit)


@router.get("/{conductor_id}", response_model=schemas.ConductorInDB)
def read_conductor(
    conductor_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene un perfil de conductor.
    Acceso permitido al mismo conductor o a un administrador.
    """
    db_conductor = crud.get_conductor(db, conductor_id)
    if not db_conductor:
        raise HTTPException(status_code=404, detail="Conductor no encontrado.")

    if not current_user.es_admin and current_user.id_usuario != db_conductor.id_usuario:
        raise HTTPException(status_code=403, detail="No autorizado.")
    
    return db_conductor


@router.post("/servicios", response_model=schemas.ConductorServicioInDB)
def add_servicio_to_conductor(
    servicio: schemas.ConductorServicioCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Asocia un servicio a un conductor.
    Solo el propio conductor (por su ID de usuario) o un admin pueden hacer esto.
    """
    db_conductor = crud.get_conductor(db, servicio.id_conductor)
    if not db_conductor:
        raise HTTPException(status_code=404, detail="Conductor no encontrado.")

    if not current_user.es_admin and current_user.id_usuario != db_conductor.id_usuario:
        raise HTTPException(status_code=403, detail="No autorizado.")

    return crud.create_conductor_servicio(db, servicio)


@router.get("/servicios/{conductor_id}", response_model=List[schemas.ConductorServicioInDB])
def get_servicios_ofrecidos(
    conductor_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Lista los servicios que ofrece un conductor.
    Accesible para cualquier usuario autenticado.
    """
    conductor = crud.get_conductor(db, conductor_id)
    if not conductor:
        raise HTTPException(status_code=404, detail="Conductor no encontrado.")

    return crud.get_servicios_by_conductor(db, conductor_id)
