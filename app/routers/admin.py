from pathlib import Path

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
