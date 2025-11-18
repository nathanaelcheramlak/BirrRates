#!/bin/bash
celery -A celery_app worker --loglevel=info > worker.log 2>&1 &
celery -A celery_app beat --loglevel=info > beat.log 2>&1 &

# Start your API
uvicorn main:app --reload
