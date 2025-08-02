from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/catalogos",
    tags=["Catálogos"],
)

# Endpoints para Tipos de Cliente
@router.get("/tipos_cliente", response_model=List[schemas.TipoCliente])
def read_tipos_cliente(db: Session = Depends(get_db)):
    return crud.get_tipos_cliente(db)

# Endpoints para Estados de Conductor
@router.get("/estados_conductor", response_model=List[schemas.EstadoConductor])
def read_estados_conductor(db: Session = Depends(get_db)):
    return crud.get_estados_conductor(db)

# Endpoints para Tipos de Vehículo
@router.get("/tipos_vehiculo", response_model=List[schemas.TipoVehiculo])
def read_tipos_vehiculo(db: Session = Depends(get_db)):
    return crud.get_tipos_vehiculo(db)

# Endpoints para Estados de Vehículo
@router.get("/estados_vehiculo", response_model=List[schemas.EstadoVehiculo])
def read_estados_vehiculo(db: Session = Depends(get_db)):
    return crud.get_estados_vehiculo(db)

# Endpoints para Tipos de Servicio
@router.get("/tipos_servicio", response_model=List[schemas.TipoServicio])
def read_tipos_servicio(db: Session = Depends(get_db)):
    return crud.get_tipos_servicio(db)

# Endpoints para Estados de Solicitud
@router.get("/estados_solicitud", response_model=List[schemas.EstadoSolicitud])
def read_estados_solicitud(db: Session = Depends(get_db)):
    return crud.get_estados_solicitud(db)
