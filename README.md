# Example backend using Helsinki profile

Uses Django and (optionally) Docker.

This project demonstrates how one can integrate a backend server to communicate with the [Helsinki profile service](https://github.com/City-of-Helsinki/open-city-profile).

This project **doesn't** demonstrate good practices about writing a Django server in general. For that check the [Django documentation](https://docs.djangoproject.com/).

## Setting the environment

By default the running environment is such that the service starts (in development mode) but it doesn't connect correctly to any authorization service it needs. To configure such a service do the following:

Copy the file `config.env.example` to a file called `config.env` and adjust settings in that file as appropriate. Also copy the file `docker-compose.override.yml.example` to a file called `docker-compose.override.yml` so that the `config.env` file gets used when running the service with `docker-compose`. Now the `config.env` file is used for reading environment variables no matter which way you choose to run the server.

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
