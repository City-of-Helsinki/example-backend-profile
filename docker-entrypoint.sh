#!/bin/sh

./manage.py migrate --noinput

./manage.py runserver --insecure 0.0.0.0:8000
