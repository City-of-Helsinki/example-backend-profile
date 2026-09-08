# Example backend using Helsinki profile

Uses Django and (optionally) Docker.

This project demonstrates how one can integrate a backend server to communicate with the [Helsinki profile service](https://github.com/City-of-Helsinki/open-city-profile).

This project **doesn't** demonstrate good practices about writing a Django server in general. For that check the [Django documentation](https://docs.djangoproject.com/).

## Setting the environment

By default the running environment is such that the service starts (in development mode)
but it doesn't connect correctly to any authorization service it needs. To configure such
a service do the following:

Copy the file `config.env.example` to a file called `config.env` and adjust settings
in that file as appropriate. Now the `config.env` file is used for reading environment
variables no matter which way you choose to run the server.

## Running with Python environment

This project uses [uv](https://docs.astral.sh/uv/) to manage the Python environment and dependencies. Install
uv by following the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

Install dependencies (including Django). This creates a `.venv` virtual environment automatically:

    uv sync

Migrate Django database (this project uses the default sqlite database):

    uv run manage.py migrate

Create admin user in order to access the admin UI (optional):

    uv run manage.py createsuperuser

Start the server:

    uv run manage.py runserver

The server should now be running in http://localhost:8000.

## Running with Docker

    docker compose up

The server should now be running in http://localhost:8081.

The Docker build doesn't automatically add an admin user so the admin UI can't be accessed unless such user is created manually.

By default, the Docker Compose setup runs the Django development server (`manage.py runserver`), which
auto-reloads on code changes thanks to the bind-mounted source directory.

### Running with uWSGI

The server mode is controlled by the `DEV_SERVER` setting in `config.env`.

To run the container with [uWSGI](https://uwsgi-docs.readthedocs.io/) instead, closer to how the
application would run in production, set `DEV_SERVER=False` in `config.env` and (re)start Compose:

    docker compose up --build

uWSGI is served directly on http://localhost:8081 (no code auto-reload; restart the container after
making changes). Switch back to the development server by setting `DEV_SERVER=True` in `config.env` again.

## Keeping Python dependencies up to date

1. Add new packages to `pyproject.toml` under `[project].dependencies` (production), `[dependency-groups].dev`
   (development) or `[dependency-groups].prod` (production-only, e.g. application servers).

2. Update `uv.lock` after changing dependencies:

       uv lock

3. To update all dependencies to their newest allowed versions, run:

       uv lock --upgrade

4. To install dependencies (including development dependencies):

       uv sync

5. To install production dependencies only:

       uv sync --no-dev --group prod

## Code formatting

This project uses [Ruff](https://docs.astral.sh/ruff/) for code formatting and quality checking. Ruff isn't
declared as a project dependency, since it's normally run through the [`pre-commit`](https://pre-commit.com/)
hooks configured in [`.pre-commit-config.yaml`](.pre-commit-config.yaml). If you want to run Ruff manually
without using pre-commit, install it separately, e.g. with `uv tool install ruff` or `pipx install ruff`.

Basic `ruff` commands:

* lint: `ruff check`
* apply safe lint fixes: `ruff check --fix`
* check formatting: `ruff format --check`
* format: `ruff format`

`pre-commit` can be used to install and run all the formatting tools as git hooks automatically before a commit.

## Endpoints

This example has two endpoints: for reading [UserData](users/models.py), and for querying Helsinki Profile. Both endpoints require authentication. The authentication is provided by bearer token which should be set in the HTTP header `Authorization`. The prefix should be `Bearer`. i.e.

`Authorization: Bearer [API token for this backend from Tunnistamo]`



### `/api/v1/myuserdata/`

Method: GET

Payload: None

Endpoint for reading the user data values saved in the database. Example response:

```json
{
  "pet_name": "Fifi",
  "birthday": "1981-02-21"
}
```

### `/api/v1/fillmybirthday/`-endpoint

Method: POST

Payload:
```json
{
  "api_token": "[Helsinki profile backend API token from Tunnistamo]"
}
```
|

An example view which uses an API token to query the users national identification number from the Helsinki Profile and saves their birthday to the `UserData`. Example response:

```json
{
  "birthday": "1981-02-21"
}
```
