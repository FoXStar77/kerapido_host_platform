from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_active_user, get_current_user

router = APIRouter(
    prefix="/solicitudes",
    tags=["Solicitudes"],
)

@router.post("/", response_model=schemas.SolicitudInDB)
def create_solicitud(
    solicitud: schemas.SolicitudCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Crea una nueva solicitud de servicio.
    Requiere autenticación de usuario activo.
    """
    # Verificar que el usuario autenticado sea un cliente
    if not current_user.es_cliente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los clientes pueden crear solicitudes."
        )

    # Buscar el objeto cliente asociado al usuario
    cliente = crud.get_cliente_by_user_id(db, usuario_id=current_user.id_usuario)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el perfil de cliente para este usuario."
        )
    
    # Asignar el ID del cliente a la solicitud
    solicitud.id_cliente = cliente.id_cliente
    
    return crud.create_solicitud(db=db, solicitud=solicitud)


@router.get("/{solicitud_id}", response_model=schemas.SolicitudInDB)
def read_solicitud(
    solicitud_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene los detalles de una solicitud específica.
    Solo el cliente que la creó o un administrador pueden verla.
    """
    db_solicitud = crud.get_solicitud(db, solicitud_id=solicitud_id)
    if db_solicitud is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitud no encontrada."
        )

    # Verificar permisos
    if not current_user.es_admin:
        cliente = crud.get_cliente_by_user_id(db, usuario_id=current_user.id_usuario)
        if cliente is None or db_solicitud.id_cliente != cliente.id_cliente:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver esta solicitud."
            )

    return db_solicitud


@router.get("/", response_model=List[schemas.SolicitudInDB])
def get_all_solicitudes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene una lista de todas las solicitudes.
    Solo accesible para administradores.
    """
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver todas las solicitudes."
        )

    return crud.get_solicitudes(db, skip=skip, limit=limit)
