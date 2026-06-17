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

**All site content lives in the `content/` directory.**

Just edit the YAML files and refresh the browser — no rebuilding required.

| YAML key | Source file | Rendered on |
|----------|-------------|-------------|
| `name`, `tagline`, `bio`, `social` | `content/profile.yaml` | Home hero, nav, footer |
| `skills` | `content/professional/skills.yaml` | Home → Skills section |
| `experience` | `content/professional/experience.yaml` | About page |
| `education` | `content/professional/education.yaml` | About page |
| `projects` | `content/professional/projects.yaml` | Projects page (Professional section) |
| `personal_projects` | `content/personal/projects.yaml` | Projects page (Personal section) |

## Project Structure

```
portfolio-site/
├── app/
│   ├── main.py              # FastAPI app, health check
│   ├── routers/
│   │   └── pages.py         # Route handlers for /, /about, /projects
│   └── templates/
│       ├── base.html        # Shared layout + CDN imports
│       ├── index.html       # Home: hero + Alpine.js skills toggle
│       ├── about.html       # Experience, education
│       └── projects.html    # Professional + personal project cards
├── static/
│   ├── css/custom.css       # Smooth scroll, card hover lift, transitions
│   └── js/interactions.js   # Parallax hero, active nav highlighting
├── content/
│   ├── profile.yaml
│   ├── professional/
│   └── personal/
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
