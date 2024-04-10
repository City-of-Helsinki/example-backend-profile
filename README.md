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

    docker compose up

The server should now be running in http://localhost:8081.

The Docker build doesn't automatically add an admin user so the admin UI can't be accessed unless such user is created manually.

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
