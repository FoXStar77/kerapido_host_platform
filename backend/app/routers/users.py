from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter()

@router.post("/users/", response_model=schemas.UsuarioInDB)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud.get_usuario_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_usuario(db=db, usuario=user)

@router.get("/users/", response_model=List[schemas.UsuarioInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_active_user)):
    users = crud.get_usuarios(db, skip=skip, limit=limit)
    return users

@router.get("/users/me/", response_model=schemas.UsuarioInDB)
def read_users_me(current_user: models.Usuario = Depends(get_current_active_user)):
    return current_user

@router.get("/users/{user_id}", response_model=schemas.UsuarioInDB)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_active_user)):
    db_user = crud.get_usuario(db, usuario_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.UsuarioInDB)
def update_user(user_id: int, user: schemas.UsuarioUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_active_user)):
    db_user = crud.update_usuario(db, usuario_id=user_id, usuario=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=schemas.UsuarioInDB)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_active_user)):
    db_user = crud.delete_usuario(db, usuario_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
