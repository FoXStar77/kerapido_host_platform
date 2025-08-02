from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(
    prefix="/conductores",
    tags=["Conductores"],
)


@router.post("/", response_model=schemas.ConductorInDB)
def create_conductor(
    conductor: schemas.ConductorCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Crea un nuevo perfil de conductor.
    Requiere autenticación de usuario activo y ser un administrador.
    """
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear perfiles de conductor."
        )

    # El usuario asociado al conductor ya debe existir
    db_usuario = crud.get_usuario(db, usuario_id=conductor.id_usuario)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario asociado no encontrado."
        )
    
    # Verificar que el usuario no tenga ya un perfil de conductor
    if db_usuario.conductor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya tiene un perfil de conductor."
        )
    
    # Asegurarse de que el usuario tenga el rol de conductor
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
    Obtiene una lista de todos los conductores.
    Solo accesible para administradores.
    """
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver todos los conductores."
        )
    return crud.get_conductores(db, skip=skip, limit=limit)


@router.get("/{conductor_id}", response_model=schemas.ConductorInDB)
def read_conductor(
    conductor_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene los detalles de un conductor específico.
    Solo el conductor o un administrador pueden ver su perfil completo.
    """
    db_conductor = crud.get_conductor(db, conductor_id=conductor_id)
    if db_conductor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conductor no encontrado."
        )

    if not current_user.es_admin and current_user.id_usuario != db_conductor.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este perfil de conductor."
        )
    
    return db_conductor


@router.post("/servicios", response_model=schemas.ConductorServicioInDB)
def add_servicio_to_conductor(
    servicio: schemas.ConductorServicioCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Asocia un tipo de servicio a un conductor.
    Solo el propio conductor o un administrador pueden realizar esta acción.
    """
    # Verificar permisos
    if not current_user.es_admin and current_user.id_usuario != servicio.id_conductor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para agregar servicios a este conductor."
        )
    
    return crud.create_conductor_servicio(db, servicio)


@router.get("/servicios/{conductor_id}", response_model=List[schemas.ConductorServicioInDB])
def get_servicios_ofrecidos(
    conductor_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene la lista de servicios que un conductor ofrece.
    """
    # Se permite ver los servicios de cualquier conductor. No se necesita permiso especial.
    return crud.get_servicios_by_conductor(db, conductor_id)
