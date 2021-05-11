#!/bin/sh

sleep 2
python manage.py migrate
python manage.py createcachetable
python manage.py load_data

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email $DJANGO_SUPERUSER_EMAIL
fi

python manage.py collectstatic --noinput
gunicorn foodster.wsgi:application --bind 0.0.0.0:8000
ls -la

exec "$@"