# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app import crud, schemas, security
from app.database import get_db
from app.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_usuario_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Nuevo endpoint para aceptar POST /auth/signup desde Flutter
@router.post("/signup", response_model=schemas.UsuarioInDB)
def registrar_cliente_desde_auth(
    registro: schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    nuevo_usuario = crud.create_usuario(db, registro)
    cliente_data = schemas.ClienteCreate(id_usuario=nuevo_usuario.id_usuario)
    crud.create_cliente(db, cliente_data)
    return nuevo_usuario
