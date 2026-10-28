# Maker night shop

## Setup

You need [uv](https://docs.astral.sh/uv/), which also installs Python, [Node.js](https://nodejs.org/) 24, and [just](https://just.systems/). With [nvm](https://github.com/nvm-sh/nvm), `nvm use` picks the Node.js version from `.nvmrc`.

1. Install the dependencies and create the database:

   ```bash
   just setup
   ```

2. Create your organizer account:

   ```bash
   just manage createsuperuser
   ```

3. Start the backend and the frontend:

   ```bash
   just dev
   ```

4. Open the shop at <http://localhost:5173/> and the admin at <http://localhost:8000/admin/>.

To list every command, run `just` without arguments.

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
