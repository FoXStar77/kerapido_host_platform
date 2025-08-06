from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.schemas import UsuarioInDB

router = APIRouter(prefix="/registro", tags=["Registro"])

@router.post("/cliente", response_model=UsuarioInDB)
def registrar_cliente(registro: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Crear usuario (con validaciones aplicadas desde el esquema)
    nuevo_usuario = crud.create_usuario(db, registro)

    # Crear cliente asociado
    cliente_data = schemas.ClienteCreate(id_usuario=nuevo_usuario.id_usuario)
    crud.create_cliente(db, cliente_data)

    return nuevo_usuario
