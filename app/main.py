from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import models
from app.database.database import engine
from app.routers import auth, pages

# Crea las tablas en la base de datos si no existen al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeCity Backend")

# Monta la carpeta 'static' para servir archivos CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluye los routers que contienen las rutas de la API y las páginas
app.include_router(auth.router)
app.include_router(pages.router)