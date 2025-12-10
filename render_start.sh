#!/bin/bash


set -e

echo "--> Apply database migrations"
python manage.py migrate

echo "--> Starting Celery Worker in background"
# Символ '&' отправляет Celery в фон, чтобы скрипт пошел дальше
# Убедитесь, что 'core' — это правильное имя вашей папки с settings.py
celery -A core worker --loglevel=info --concurrency=2 &

echo "--> Starting Gunicorn (Web Server)"
# Эта команда работает на переднем плане и держит контейнер активным
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
