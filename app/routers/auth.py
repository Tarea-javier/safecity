# Contenido completo para app/routers/auth.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import security
from app.database import crud
from app.dependencies import get_db
from app.schemas import user as user_schemas

router = APIRouter(tags=["Authentication & Users"])

@router.post("/token") # Ya no necesita response_model porque la respuesta es directa.
async def login_for_access_token(
    response: Response, # Añadimos el objeto Response para poder establecer la cookie.
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = crud.get_user(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # --- Cambio Clave: Establecer la Cookie ---
    # Esto le dice al navegador que guarde el token y lo envíe en futuras peticiones.
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True,  # Hace que la cookie no sea accesible desde JavaScript (más seguro).
        samesite="lax", # Ayuda a proteger contra ataques CSRF.
        secure=False    # En un entorno de producción con HTTPS, esto debería ser True.
    )
    
    # Devolvemos una respuesta simple de éxito para que el JavaScript sepa que el login funcionó.
    return {"status": "success"}

@router.post("/users/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
def create_user_registration(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)