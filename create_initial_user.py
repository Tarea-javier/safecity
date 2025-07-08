from app.database.database import SessionLocal, engine
from app.database import models
from app.security import get_password_hash

# Crea las tablas en la base de datos
print("Creando tablas en la base de datos...")
models.Base.metadata.create_all(bind=engine)
print("Tablas creadas.")

db = SessionLocal()

# Verifica si el usuario ya existe
db_user = db.query(models.User).filter(models.User.username == "admin").first()

if not db_user:
    # Crea un nuevo usuario
    new_user = models.User(
        username="admin", 
        hashed_password=get_password_hash("password123")
    )
    db.add(new_user)
    db.commit()
    print("Usuario 'admin' con contraseña 'password123' creado exitosamente.")
else:
    print("El usuario 'admin' ya existe.")

db.close()