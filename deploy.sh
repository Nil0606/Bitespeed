#!/bin/bash

# Run make migration
echo "Running make migration..."
python manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Run Gunicorn server
echo "Starting Gunicorn server..."
gunicorn core.wsgi
