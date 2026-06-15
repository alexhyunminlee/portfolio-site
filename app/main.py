import yaml
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.routers import pages

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Portfolio Site")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")

app.include_router(pages.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/fun-facts", response_class=HTMLResponse)
async def fun_facts():
    content_path = BASE_DIR / "content" / "portfolio.yaml"
    with open(content_path, "r") as f:
        data = yaml.safe_load(f)

    facts = data.get("fun_facts", [])
    items = "".join(f"<li class='fun-fact-item'>{fact}</li>" for fact in facts)
    return f"""
<ul class="fun-facts-list">
  {items}
</ul>
"""


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
