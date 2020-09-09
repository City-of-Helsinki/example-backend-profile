# Example backend using Helsinki profile

Uses Django and (optionally) Docker.

This project demonstrates how one can integrate a backend server to communicate with the [Helsinki profile service](https://github.com/City-of-Helsinki/open-city-profile).

This project **doesn't** demonstrate good practices about writing a Django server in general. For that check the [Django documentation](https://docs.djangoproject.com/).

## Running with (virtual) Python environment

Install Python virtual environment:

    python3 -m venv .venv

Activate it:

    source .venv/bin/activate

Install requirements (including Django):

    pip install -r requirements.txt

Migrate Django database (this project uses the default sqlite database):

    ./manage.py migrate

Create admin user in order to access the admin UI (optional):

    ./manage.py createsuperuser

Start the server:

    ./manage.py runserver

The server should now be running in http://localhost:8000.

## Running with Docker

    docker-compose up

The server should now be running in http://localhost:8000.

The Docker build doesn't automatically add an admin user so the admin UI can't be accessed unless such user is created manually.
