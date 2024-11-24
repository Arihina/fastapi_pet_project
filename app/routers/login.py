from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.config import settings

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_user(username: str, password: str):
    if username == "admin" and password == settings.ADMIN_PASSWORD:
        return "admin"
    elif username == "storekeeper" and password == settings.STOREKEEPER_PASSWORD:
        return "storekeeper"
    else:
        return None


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    role = verify_user(form_data.username, form_data.password)

    if not role:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if role == "admin":
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/storekeeper", status_code=status.HTTP_303_SEE_OTHER)
