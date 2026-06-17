# Portfolio site task runner
# Run `just` to see available commands, `just <command>` to run one.

# Default: list all commands
default:
    @just --list

# ── Development ────────────────────────────────────────────────────────────────

# Start the dev server with live reload
dev:
    uvicorn app.main:app --reload

# ── Code quality ───────────────────────────────────────────────────────────────

# Check formatting and linting (non-destructive — reports issues only)
check:
    python3 -m ruff check app/
    python3 -m ruff format --check app/

# Fix all auto-fixable lint issues and reformat code in place
fix:
    python3 -m ruff check --fix app/
    python3 -m ruff format app/

# ── Dependencies ───────────────────────────────────────────────────────────────

# Install all dependencies into the active virtualenv
install:
    pip install -r requirements.txt

# ── Deployment ─────────────────────────────────────────────────────────────────

# Build the Docker image
docker-build:
    docker build -t portfolio-site .

# Run the Docker container locally
docker-run:
    docker run -p 8000:8000 --env-file .env portfolio-site
