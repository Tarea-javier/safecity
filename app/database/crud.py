from sqlalchemy.orm import Session
from . import models
from .. import security
from ..schemas import user as user_schemas

def get_user(db: Session, username: str):
    """Busca y devuelve un usuario por su nombre de usuario."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: user_schemas.UserCreate):
    """Crea un nuevo usuario en la base de datos."""
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user