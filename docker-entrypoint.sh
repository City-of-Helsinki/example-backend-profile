#!/bin/sh

./manage.py migrate --noinput

./manage.py runserver 0.0.0.0:8000
