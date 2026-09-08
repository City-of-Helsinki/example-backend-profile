#!/bin/sh

./manage.py migrate --noinput

# Match django-environ's boolean parsing (case-insensitive; true/on/ok/y/yes/1 are truthy).
dev_server_flag=$(printf '%s' "$DEV_SERVER" | tr '[:upper:]' '[:lower:]')

case "$dev_server_flag" in
    true | on | ok | y | yes | 1)
        exec ./manage.py runserver --insecure 0.0.0.0:8000
        ;;
    *)
        exec uwsgi \
            --module example_backend_profile.wsgi:application \
            --http 0.0.0.0:8000 \
            --master \
            --processes 2 \
            --threads 2
        ;;
esac
