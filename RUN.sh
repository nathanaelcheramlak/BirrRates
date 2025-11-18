#!/bin/bash

# Install Dependencies
pip install -r requirements.txt

apt-get update
apt-get install -y redis-server

# Start Redis
redis-server --daemonize yes

# Start Celery worker
celery -A celery_app worker --loglevel=info &

# Start Celery beat
celery -A celery_app beat --loglevel=info &

# Keep script running
wait
