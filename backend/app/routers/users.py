# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
)


@router.post("/", response_model=schemas.UsuarioInDB, status_code=201)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud.get_usuario_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")
    return crud.create_usuario(db=db, usuario=user)


@router.get("/", response_model=List[schemas.UsuarioInDB])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    if not current_user.es_admin:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return crud.get_usuarios(db, skip=skip, limit=limit)


@router.get("/me", response_model=schemas.UsuarioInDB)
def read_users_me(current_user: models.Usuario = Depends(get_current_active_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.UsuarioInDB)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    if not current_user.es_admin and current_user.id_usuario != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    db_user = crud.get_usuario(db, usuario_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@router.put("/{user_id}", response_model=schemas.UsuarioInDB)
def update_user(
    user_id: int,
    user: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    if not current_user.es_admin and current_user.id_usuario != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    db_user = crud.get_usuario(db, usuario_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return crud.update_usuario(db, usuario_id=user_id, usuario=user)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user),
):
    if not current_user.es_admin and current_user.id_usuario != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    db_user = crud.get_usuario(db, usuario_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    crud.delete_usuario(db, usuario_id=user_id)
    return  # 204 No Content → sin body
