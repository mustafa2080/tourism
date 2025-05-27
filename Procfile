web: bash start.sh
release: DJANGO_SETTINGS_MODULE=railway_settings python manage.py migrate --noinput && DJANGO_SETTINGS_MODULE=railway_settings python manage.py collectstatic --noinput
