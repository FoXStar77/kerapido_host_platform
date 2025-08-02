from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(
    prefix="/transacciones_pago",
    tags=["Pagos"],
)

@router.post("/", response_model=schemas.TransaccionPagoInDB)
def create_transaccion_pago(
    transaccion: schemas.TransaccionPagoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Crea una nueva transacción de pago.
    """
    return crud.create_transaccion_pago(db=db, transaccion=transaccion)

@router.get("/{transaccion_id}", response_model=schemas.TransaccionPagoInDB)
def read_transaccion_pago(
    transaccion_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    """
    Obtiene los detalles de una transacción de pago específica.
    """
    db_transaccion = crud.get_transaccion_pago(db, transaccion_id)
    if not db_transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción de pago no encontrada."
        )

    # Solo el usuario que inició la transacción o un administrador pueden verla
    if not current_user.es_admin and current_user.id_usuario != db_transaccion.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta transacción."
        )

    return db_transaccion
