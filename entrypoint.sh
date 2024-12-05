#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting the application..."
exec "$@"