#!/bin/bash
# Start Celery worker and beat
pip install -r requirements.txt
celery -A celery_app worker --loglevel=info &
celery -A celery_app beat --loglevel=info &
wait
