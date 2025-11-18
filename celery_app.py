import os
from celery import Celery
from celery.schedules import crontab
from scraper.scrape import scrape_all
from dotenv import load_dotenv
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
if not REDIS_URL:
    raise ValueError("REDIS_URL is not set in environment variables.")

celery = Celery(
    "my_app",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.timezone = "UTC"
celery.conf.enable_utc = True

@celery.task
def scraper():
    print("Cron Job Started!")
    scrape_all()
    print("Cron Job Finished!")

celery.conf.beat_schedule = {
    "run-every-8-hours": {
        "task": "celery_app.scraper",
        "schedule": crontab(hour="*/8"),
    },
}
