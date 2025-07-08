# Contenido completo para app/dependencies.py

from fastapi import Depends, HTTPException, status, Cookie
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import crud, models
from app.database.database import SessionLocal
from app.schemas import user as user_schemas
from app.security import SECRET_KEY, ALGORITHM

def get_db():
    """Dependencia para obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    access_token: str | None = Cookie(default=None), 
    db: Session = Depends(get_db)
):
    """
    Decodifica el token JWT obtenido de la cookie para obtener el usuario actual.
    Esta es la dependencia que protegerá nuestras rutas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if access_token is None:
        raise credentials_exception

    # El valor de la cookie es "Bearer <token>", necesitamos separar el token real.
    try:
        token_parts = access_token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
            raise credentials_exception
        token = token_parts[1]
    except:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user