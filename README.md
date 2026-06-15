# Portfolio Site

A personal portfolio website for a **Data Scientist & Mechanical Engineer**, built with **FastAPI**, **Jinja2**, **Tailwind CSS**, **Alpine.js**, and **HTMX**. No build step required — just Python and a browser.

## Overview

| Feature | How it works |
|---------|-------------|
| Server-side rendering | FastAPI + Jinja2 templates |
| Styling | Tailwind CSS via CDN |
| Micro-interactions | Alpine.js (skills toggle, project detail expand) |
| Progressive enhancement | HTMX lazy-loads the "Fun Facts" section |
| Content management | Edit a single `content/portfolio.yaml` file |
| Deployment | Render (via `render.yaml`) or any Docker host |

## Local Development

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd portfolio-site
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env if needed — defaults work for local dev
```

### 5. Run the dev server

```bash
uvicorn app.main:app --reload
# or: python -m app.main
```

Open [http://localhost:8000](http://localhost:8000).

The `--reload` flag restarts the server automatically when you change Python files.

## Editing Content

**All site content lives in `content/portfolio.yaml`.**

Just edit the YAML and refresh the browser — no rebuilding required.

| YAML key | Rendered on |
|----------|-------------|
| `name`, `tagline`, `bio` | Home hero, nav, footer |
| `skills` | Home → Skills section |
| `experience` | About page |
| `education` | About page |
| `fun_facts` | About page (HTMX lazy-loaded) |
| `projects` | Projects page |
| `social` | Footer links |

## Project Structure

```
portfolio-site/
├── app/
│   ├── main.py              # FastAPI app, health check, /api/fun-facts
│   ├── routers/
│   │   └── pages.py         # Route handlers for /, /about, /projects
│   └── templates/
│       ├── base.html        # Shared layout + CDN imports
│       ├── index.html       # Home: hero + Alpine.js skills toggle
│       ├── about.html       # Experience, education, HTMX fun facts
│       └── projects.html    # Project cards with Alpine.js expand panels
├── static/
│   ├── css/custom.css       # Smooth scroll, card hover lift, transitions
│   └── js/interactions.js   # Parallax hero, active nav highlighting
├── content/
│   └── portfolio.yaml       # ← Edit this to update all content
├── requirements.txt
├── .env.example
├── Dockerfile
├── render.yaml
└── README.md
```

## Deploying to Render

1. Push this repo to GitHub.
2. Log in to [Render](https://render.com) and click **New → Web Service**.
3. Connect your GitHub repository.
4. Render automatically detects `render.yaml` and pre-fills all settings.
5. Click **Deploy** — your site will be live at a `*.onrender.com` URL within minutes.

To use a custom domain, go to **Settings → Custom Domains** in your Render dashboard.

## Docker

```bash
# Build
docker build -t portfolio-site .

# Run
docker run -p 8000:8000 --env-file .env portfolio-site
```

## License

MIT
