# Maker night shop

## Setup

You need [uv](https://docs.astral.sh/uv/), which also installs Python, [Node.js](https://nodejs.org/) 24, and [just](https://just.systems/). With [nvm](https://github.com/nvm-sh/nvm), `nvm use` picks the Node.js version from `.nvmrc`.

1. Install the dependencies and create the database:

   ```bash
   just setup
   ```

2. Create an account to log into the Django admin. The command asks for a username, an email address (optional) and a password:

   ```bash
   just manage createsuperuser
   ```

3. Start the backend and the frontend:

   ```bash
   just dev
   ```

4. Open the shop at <http://localhost:5173/> and the admin at <http://localhost:8000/admin/>.

To list every command, run `just` without arguments.

## Test and lint

- `just test` runs the backend and frontend tests.
- `just lint` runs ruff, mypy, Prettier, ESLint and the TypeScript compiler. `just format` fixes what it can.
- After changing the API, run `just generate-api` and commit its two files. `just check-api` fails when they're out of date.
- After changing a model, run `just manage makemigrations` and commit the migration. `just check-migrations` fails when one is missing.
- `just check-all` runs everything the CI on GitHub checks: the lock file, lint, the tests, `check-api` and `check-migrations`.

## Layout

```
backend/
  api/            shared API code: errors, access levels, API description
  config/         settings and URLs
  tests/          tests over HTTP
  manage.py       Django's command-line tool, run with just manage
frontend/
  openapi.json    the API description, written by just generate-api
  src/            the React app; src/api/schema.d.ts is written by just generate-api
  tests/          page tests
justfile          the project's commands
pyproject.toml    Python dependencies and tool settings
```
