set shell := ["bash", "-uc"]

# `just` without a command lists them all
[private]
default:
    @just --list

# Installs everything and creates or updates the database
setup: setup-backend

# Python dependencies and database migrations
setup-backend:
    uv sync
    just manage migrate

# Starts Django on port 8000
backend:
    cd backend && DEBUG=true uv run python manage.py runserver

# Django's management commands, for example `just manage createsuperuser`
manage *args:
    cd backend && uv run python manage.py {{ args }}

# Runs every test
test: test-backend

# Extra arguments go to pytest, for example `just test-backend backend/tests/test_admin.py`
test-backend *args:
    uv run pytest {{ args }}

# Formats the code and fixes what the linters can fix
format:
    uv run ruff format .
    uv run ruff check --fix .

# Runs every linter and type check
lint: lint-backend

# ruff and mypy
lint-backend:
    uv run ruff check .
    uv run ruff format --check .
    uv run mypy
