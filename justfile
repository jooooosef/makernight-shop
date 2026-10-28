set shell := ["bash", "-uc"]

# `just` without a command lists them all
[private]
default:
    @just --list

# Installs everything and creates or updates the database
setup: setup-backend setup-frontend

# Python dependencies and database migrations
setup-backend:
    uv sync
    just manage migrate

# Node dependencies
setup-frontend:
    cd frontend && npm ci

# Starts Django on port 8000 and Vite on port 5173, which passes /api on to Django
[parallel]
dev: backend frontend

# Starts Django on port 8000
backend:
    cd backend && DEBUG=true uv run python manage.py runserver

# Starts Vite on port 5173
frontend:
    cd frontend && npm run dev

# Django's management commands, for example `just manage createsuperuser`
manage *args:
    cd backend && uv run python manage.py {{ args }}

# Runs every test
test: test-backend test-frontend

# Extra arguments go to pytest, for example `just test-backend backend/tests/test_admin.py`
test-backend *args:
    uv run pytest {{ args }}

# Extra arguments go to Vitest, for example `just test-frontend tests/App.test.tsx`
test-frontend *args:
    cd frontend && npx vitest run {{ args }}

# Formats the code and fixes what the linters can fix
format:
    uv run ruff format .
    uv run ruff check --fix .
    cd frontend && npm run format

# Runs every linter and type check
lint: lint-backend lint-frontend

# ruff and mypy
lint-backend:
    uv run ruff check .
    uv run ruff format --check .
    uv run mypy

# Prettier, ESLint and TypeScript
lint-frontend:
    cd frontend && npm run format:check
    cd frontend && npm run lint

# Writes the API description and the frontend's types from it
generate-api:
    just manage spectacular --format openapi-json --validate --fail-on-warn --file ../frontend/openapi.json
    cd frontend && npx openapi-typescript openapi.json -o src/api/schema.d.ts

# Fails when the committed API description or types are out of date
check-api: generate-api
    git diff --exit-code -- frontend/openapi.json frontend/src/api/schema.d.ts
