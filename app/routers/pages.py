from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.content import load_portfolio

BASE_DIR = Path(__file__).resolve().parent.parent.parent

router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")


@router.get("/")
async def index(request: Request):
    data = load_portfolio()
    return templates.TemplateResponse(
        "index.html", {"request": request, "portfolio": data}
    )


@router.get("/about")
async def about(request: Request):
    data = load_portfolio()
    return templates.TemplateResponse(
        "about.html", {"request": request, "portfolio": data}
    )


@router.get("/projects")
async def projects(request: Request):
    data = load_portfolio()
    return templates.TemplateResponse(
        "projects.html", {"request": request, "portfolio": data}
    )
