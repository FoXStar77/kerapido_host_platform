# app/routers/catalogos.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/catalogos",
    tags=["Catálogos"],
)


@router.get("/tipos_cliente", response_model=List[schemas.TipoClienteSchema])
def read_tipos_cliente(db: Session = Depends(get_db)):
    return crud.get_tipos_cliente(db)


@router.get("/estados_conductor", response_model=List[schemas.EstadoConductorSchema])
def read_estados_conductor(db: Session = Depends(get_db)):
    return crud.get_estados_conductor(db)


@router.get("/tipos_vehiculo", response_model=List[schemas.TipoVehiculoSchema])
def read_tipos_vehiculo(db: Session = Depends(get_db)):
    return crud.get_tipos_vehiculo(db)


@router.get("/estados_vehiculo", response_model=List[schemas.EstadoVehiculoSchema])
def read_estados_vehiculo(db: Session = Depends(get_db)):
    return crud.get_estados_vehiculo(db)


@router.get("/tipos_servicio", response_model=List[schemas.TipoServicioSchema])
def read_tipos_servicio(db: Session = Depends(get_db)):
    return crud.get_tipos_servicio(db)


@router.get("/estados_solicitud", response_model=List[schemas.EstadoSolicitudSchema])
def read_estados_solicitud(db: Session = Depends(get_db)):
    return crud.get_estados_solicitud(db)
