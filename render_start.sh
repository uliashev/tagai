#!/bin/bash

set -e

echo "--> Apply database migrations"
python manage.py migrate

echo "--> Starting Celery Worker in background"
# ИСПРАВЛЕНО: используем 'config', так как celery.py лежит там
celery -A config worker --loglevel=debug --concurrency=1 &

echo "--> Starting Gunicorn (Web Server)"
# ИСПРАВЛЕНО: путь к wsgi теперь 'config.wsgi'
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT