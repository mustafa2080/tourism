#!/bin/bash

# Start script for Railway deployment

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting application on port $PORT"

# Set Django settings module for Railway
export DJANGO_SETTINGS_MODULE=railway_settings

echo "Using Django settings: $DJANGO_SETTINGS_MODULE"

# Run migrations (in case they weren't run in deploy phase)
echo "Running database migrations..."
python3 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Setup initial data
echo "Setting up initial data..."
python3 manage.py setup_initial_data

# Start gunicorn
echo "Starting gunicorn server..."
exec gunicorn tourism_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
