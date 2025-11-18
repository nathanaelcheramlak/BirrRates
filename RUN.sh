#!/bin/bash
# Start Celery worker and beat
celery -A celery_app worker --loglevel=info &
celery -A celery_app beat --loglevel=info &
wait
