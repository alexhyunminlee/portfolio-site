import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import pages

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Portfolio Site")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")

app.include_router(pages.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
