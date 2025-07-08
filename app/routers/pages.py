from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dependencies import get_current_user
from app.database.models import User

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root():
    """Redirige la raíz a la página de login."""
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@router.get("/login", response_class=HTMLResponse)
async def read_login_form(request: Request):
    """Muestra la página de login."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def read_register_form(request: Request):
    """Muestra la página de registro."""
    return templates.TemplateResponse("register.html", {"request": request})
    
@router.get("/map", response_class=HTMLResponse)
async def read_main_map(request: Request, current_user: User = Depends(get_current_user)):
    """
    Sirve la página principal del mapa.
    Esta ruta está PROTEGIDA: solo se puede acceder con un token JWT válido.
    """
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})