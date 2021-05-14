#!/bin/sh

sleep 2

python3 manage.py migrate
python3 manage.py migrate recipes
python3 manage.py createcachetable
python3 manage.py load_data

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python3 manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email $DJANGO_SUPERUSER_EMAIL
fi

python3 manage.py collectstatic --noinput
gunicorn foodster.wsgi:application --bind 0.0.0.0:8000
ls -la

exec "$@"
