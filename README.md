# Maker night shop

## Setup

You need [uv](https://docs.astral.sh/uv/), which also installs Python, and [just](https://just.systems/).

1. Install the dependencies and create the database:

   ```bash
   just setup
   ```

2. Create your organizer account:

   ```bash
   just manage createsuperuser
   ```

3. Start the backend:

   ```bash
   just backend
   ```

4. Log in to the admin at <http://localhost:8000/admin/>.

To list every command, run `just` without arguments.

## Layout

```
backend/
  config/         settings and URLs
  tests/          tests over HTTP
  manage.py       Django's command-line tool, run with `just manage`
justfile          the project's commands
pyproject.toml    Python dependencies and tool settings
```
