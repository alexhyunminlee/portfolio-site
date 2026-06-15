import yaml
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent.parent

router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")


def load_portfolio() -> dict:
    content_path = BASE_DIR / "content" / "portfolio.yaml"
    with open(content_path, "r") as f:
        return yaml.safe_load(f)


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
