from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from . import models, crud, security
from jose import JWTError, jwt
from .config import settings
from app.models import Usuario



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = security.schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_usuario_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.Usuario = Depends(get_current_user)):
    if not current_user.email_verificado:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def conductor_owner_or_admin(user_id_objetivo: int, current_user: Usuario):
    if not current_user.es_admin and current_user.id_usuario != user_id_objetivo:
        raise HTTPException(403, detail="No autorizado")
